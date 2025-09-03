# authentication/serializers.py
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from .models import User

class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        help_text="Enter a valid email address"
    )
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=50)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=50)
    password = serializers.CharField(
        write_only=True,
        min_length=6,
        style={'input_type': 'password'},
        help_text="Password must be at least 6 characters long"
    )
    password2 = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text="Enter the same password as above for verification"
    )

    def validate(self, attrs):
        """Validate that passwords match"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    # def validate_email(self, value):
    #     """Validate that email is unique"""
    #     if User.objects.filter(email=value).exists():
    #         raise serializers.ValidationError("A user with this email already exists.")
    #     return value

    def create(self, validated_data):
        """Create and return a new user"""
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        help_text="Enter your registered email address"
    )
    password = serializers.CharField(
        style={'input_type': 'password'},
        help_text="Enter your password"
    )

    def validate(self, attrs):
        """Validate user credentials"""
        email = attrs.get('email')
        password = attrs.get('password')

        if email or not password:
            raise serializers.ValidationError('Must include "email" and "password".')
            
            user = User.objects(email=email).first()
            if not user:
                raise serializers.ValidationError('Invalid email or password.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
        else:
            raise serializers.ValidationError('Must include "email" and "password".')

        attrs['user'] = user
        return attrs

class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)