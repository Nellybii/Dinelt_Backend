from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from foodie_app.models import (
    User, Profile, Post, Story, Restaurant, RestaurantReview, Food, Order,
    Reservation, Cart, OrderItem, Booking, Accommodation, Manager, CartItem
)
import logging
from datetime import timedelta
from django.utils import timezone

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
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password'),
        }

        user = authenticate(**credentials)

        if user is None:
            logger.error(f"Authentication failed for email: {credentials['email']}")
            raise serializers.ValidationError({'detail': 'Invalid email or password'}, code='authorization')

        if not user.is_active:
            logger.error(f"Inactive user account attempted to login: {user.email}")
            raise serializers.ValidationError({'detail': 'User account is disabled'}, code='authorization')

        return super().validate(attrs)
    

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password',
            'full_name', 'phone_number', 'country', 'city', 'address', 'postal_code', 'image', 'is_business_owner',
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

            profile_data = {
                'user': user,
                'username': user.username,
                'image': validated_data.get('image')  
            }
            Profile.objects.create(**profile_data)
            logger.info(f"User and profile created successfully: {user.email}")

            return user
        except Exception as e:
            logger.error(f"Error creating user and profile: {e}")
            raise serializers.ValidationError("User and profile created successfully")

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'image', 'created_at', 'comments', 'likes']
        read_only_fields = ['author', 'comments', 'likes']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        validated_data['author'] = user 
        post = super().create(validated_data)

        self._update_profile(user, post)

        return post

    def _update_profile(self, user, post):
        profile = Profile.objects.get(user=user)
        profile.posts.add(post)
        profile.save()


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['id', 'author', 'content', 'image', 'created_at', 'expires_at', 'comments', 'likes']
        read_only_fields = ['author', 'comments', 'likes', 'expires_at', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        validated_data['author'] = user 
        validated_data['expires_at'] = timezone.now() + timedelta(hours=24)
        
        story = super().create(validated_data)
        
        profile = Profile.objects.get(user=user)
        profile.stories.add(story)
        profile.save()  

        return story


class ProfileSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    stories = StorySerializer(many=True, read_only=True)
    is_business_owner = serializers.BooleanField(source='user.is_business_owner', read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'username', 'bio', 'image', 'followers_number', 'following', 'posts', 'stories', 'is_business_owner']
        read_only_fields = ['user', 'posts', 'stories', 'followers_number', 'following', 'is_business_owner']
        
class RestaurantReviewSerializer(serializers.ModelSerializer): 
    class Meta:
        model = RestaurantReview
        fields = ['id', 'restaurant', 'user', 'rating', 'review', 'created_at']

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'city', 'country', 'address', 'phone_number', 'image', 'description']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        if not user.is_business_owner:
            raise serializers.ValidationError("You must be a business owner to create a restaurant.")

        return super().create(validated_data)

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'restaurant', 'name', 'description', 'price', 'category']
        read_only_fields = ['owner']


# class FoodSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Food
#         fields = '__all__'  

class OrderItemSerializer(serializers.ModelSerializer):
    food_name = serializers.ReadOnlyField(source='food.name')

    class Meta:
        model = OrderItem
        fields = ['id', 'food', 'food_name', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'restaurant', 'status', 'order_time', 'estimated_delivery_time', 'total_price', 'order_items']
        read_only_fields = ['id', 'user', 'order_time', 'estimated_delivery_time', 'total_price']

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        return order

class CartItemSerializer(serializers.ModelSerializer):
    food_name = serializers.CharField(source='food.name', read_only=True)
    food_price = serializers.DecimalField(source='food.price', max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'food', 'food_name', 'food_price', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.total_price

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'cart_items', 'total_price']
        read_only_fields = ['id', 'user', 'total_price']
    
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'restaurant', 'reservation_date', 'number_of_people', 'special_requests', 'reservation_type']
        read_only_fields = ['id', 'user']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'accommodation', 'check_in_date', 'check_out_date', 'number_of_guests', 'special_requests']
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        try:
            booking = super().create(validated_data)
            logger.info(f"Booking created successfully for user: {booking.user.username}")
            return booking
        except Exception as e:
            logger.error(f"Error creating booking: {e}")
            raise serializers.ValidationError("An error occurred while creating the booking.")
    def validate_accommodation(self, value):
        if not Accommodation.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Accommodation does not exist.")
        return value
    
class AccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        fields = ['id', 'name', 'address', 'city', 'country', 'description', 'image', 'restaurant', 'price_per_night']
        read_only_fields = ['id']

    def create(self, validated_data):
        try:
            accommodation = super().create(validated_data)
            logger.info(f"Accommodation created successfully: {accommodation.name}")
            return accommodation
        except Exception as e:
            logger.error(f"Error creating accommodation: {e}")
            raise serializers.ValidationError("An error occurred while creating the accommodation.")


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ['id', 'user', 'restaurant', 'date_assigned']
        read_only_fields = ['id', 'date_assigned']
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        if not user.is_business_owner:
            raise serializers.ValidationError("You must be a business owner to assign a manager.")

        manager = super().create(validated_data)
        return manager
