from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from foodie_app.models import User, Profile, Post, Story, Restaurant, MenuItem, OrderItem, Order, Reservation

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
            raise serializers.ValidationError('Invalid email or password')

        if not user.is_active:
            raise serializers.ValidationError('User account is disabled')

        return super().validate(attrs)



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password',
            'full_name', 'phone_number', 'country', 'city', 'address', 'postal_code', 'image'
        )
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'image', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']


class StorySerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Story
        fields = ['id', 'author', 'content', 'image', 'created_at' ]
        read_only_fields = ['id', 'author', 'created_at']


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'username', 'bio', 'image', 'followers', 'following', 'posts']
        read_only_fields = ['id', 'user', 'followers', 'following', 'posts']

    def update(self, instance, validated_data):
        if 'image' in validated_data:
            instance.image.delete(save=False) 
        return super().update(instance, validated_data)
    

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
        fields = ['menu_item', 'quantity','price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'restaurant', 'items', 'total_price', 'created_at', 'status']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'restaurant', 'reservation_date', 'number_of_people', 'special_requests']