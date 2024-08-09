from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from foodie_app.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email','image', 'full_name', 'phone_number', 
            'country', 'city', 'address', 'postal_code'
        )

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        profile = user.get_profile()  
        token['full_name'] = profile.full_name
        token['username'] = user.username
        token['email'] = user.email
        token['bio'] = profile.bio
        token['image'] = str(profile.image)
        token['verified'] = profile.verified
        
        return token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    # image = serializers.ImageField(required=True)
    full_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    country = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    postal_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'email', 'username', 'password', 'password2',
            'full_name', 'phone_number', 'country',
            'city', 'address', 'postal_code'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            full_name=validated_data['full_name'],
            phone_number=validated_data['phone_number'],
            country=validated_data['country'],
            city=validated_data['city'],
            address=validated_data['address'],
            postal_code=validated_data['postal_code']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
