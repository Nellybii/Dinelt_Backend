from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from foodie_app.models import User, Profile, Post, Story, Restaurant, MenuItem, OrderItem, Order, Reservation
import logging

logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'image', 'full_name', 'phone_number',
            'country', 'city', 'address', 'postal_code'
        )
        extra_kwargs = {'password': {'write_only': True}}

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        try:
            credentials = {
                'email': attrs.get('email'),
                'password': attrs.get('password'),
            }

            user = authenticate(**credentials)

            if user is None:
                logger.error(f"Authentication failed for email: {attrs.get('email')}")
                raise serializers.ValidationError('Invalid email or password')

            if not user.is_active:
                logger.error(f"Inactive user account attempted to login: {user.email}")
                raise serializers.ValidationError('User account is disabled')

            return super().validate(attrs)

        except Exception as e:
            logger.error(f"Error during token obtain: {e}")
            raise serializers.ValidationError("An error occurred during authentication")

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password',
            'full_name', 'phone_number', 'country', 'city', 'address', 'postal_code', 'image'
        )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            logger.warning(f"Attempt to register with existing email: {value}")
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            logger.warning(f"Attempt to register with existing username: {value}")
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def create(self, validated_data):
        try:
            password = validated_data.pop('password')
            user = User(**validated_data)
            user.set_password(password)
            user.save()
            
            # Automatically create a profile for the new user
            Profile.objects.create(user=user)
            logger.info(f"User and profile created successfully: {user.email}")
            
            return user
        except Exception as e:
            logger.error(f"Error creating user and profile: {e}")
            raise serializers.ValidationError("User and profile created successfully")

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'image', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']

    def validate(self, data):
        if not data.get('content') and not data.get('image'):
            logger.warning("Post creation failed due to missing content and image.")
            raise serializers.ValidationError("Post must contain either content or an image.")
        return data

class StorySerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Story
        fields = ['id', 'author', 'content', 'image', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']

    def validate(self, data):
        if not data.get('content') and not data.get('image'):
            logger.warning("Story creation failed due to missing content and image.")
            raise serializers.ValidationError("Story must contain either content or an image.")
        return data

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'username', 'bio', 'image', 'followers', 'following', 'posts']
        read_only_fields = ['id', 'user', 'followers', 'following', 'posts']

    def update(self, instance, validated_data):
        try:
            if 'image' in validated_data:
                instance.image.delete(save=False) 
            updated_instance = super().update(instance, validated_data)
            logger.info(f"Profile updated successfully for user: {updated_instance.user}")
            return updated_instance
        except Exception as e:
            logger.error(f"Error updating profile: {e}")
            raise serializers.ValidationError("An error occurred while updating the profile.")

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'image']

class RestaurantSerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'city', 'country' ,'address', 'phone_number', 'image', 'description', 'menu_items']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'restaurant', 'items', 'total_price', 'created_at', 'status']

    def create(self, validated_data):
        try:
            items_data = validated_data.pop('items')
            order = Order.objects.create(**validated_data)
            for item_data in items_data:
                OrderItem.objects.create(order=order, **item_data)
            logger.info(f"Order created successfully for user: {order.user}")
            return order
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            raise serializers.ValidationError("An error occurred while creating the order.")

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'restaurant', 'reservation_date', 'number_of_people', 'special_requests']

    def create(self, validated_data):
        try:
            reservation = super().create(validated_data)
            logger.info(f"Reservation created successfully for user: {reservation.user}")
            return reservation
        except Exception as e:
            logger.error(f"Error creating reservation: {e}")
            raise serializers.ValidationError("An error occurred while creating the reservation.")
