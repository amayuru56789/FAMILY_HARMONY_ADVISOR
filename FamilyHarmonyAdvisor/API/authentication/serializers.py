# authentication/serializers.py
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from django.core.validators import RegexValidator, validate_email
from django.core.exceptions import ValidationError
from .models import User, UserManager
import re

def normalize_email(email):
    """
    Standalone function to normalize email
    """
    email = email or ''
    try:
        email_name, domain_part = email.strip().rsplit('@', 1)
    except ValueError:
        return email.lower()
    else:
        return email_name.lower() + '@' + domain_part.lower()

class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        help_text="Enter a valid email address"
    )
    first_name = serializers.CharField(
        required=False, 
        allow_blank=True, 
        max_length=50,
        # validators=[RegexValidator(
        #     regex='^[a-zA-Z]+$',
        #     message='First name should contain only letters',
        #     code='invalid_first_name'
        # )]
        )
    last_name = serializers.CharField(
        required=False, 
        allow_blank=True, 
        max_length=50
        # validators=[RegexValidator(
        #     regex='^[a-zA-Z]+$',
        #     message='Last name should contain only letters',
        #     code='invalid_last_name'
        # )]
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'},
        help_text="Password must be at least 8 characters long"
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
        
         # Additional password strength validation
        password = attrs['password']
        if not re.search(r'[A-Z]', password):
            raise serializers.ValidationError({"password": "Password must contain at least one uppercase letter."})
        if not re.search(r'[a-z]', password):
            raise serializers.ValidationError({"password": "Password must contain at least one lowercase letter."})
        if not re.search(r'[0-9]', password):
            raise serializers.ValidationError({"password": "Password must contain at least one digit."})
            
        return attrs
        

    def validate_email(self, value):
        """Validate that email is unique"""

        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format.")
        
        # Normalize email using our standalone function
        normalized_email = normalize_email(value)
        
        if User.objects.filter(email=normalized_email).first():
            raise serializers.ValidationError("A user with this email already exists.")
        return normalized_email  # Return the normalized email

    def validate_first_name(self, value):
        """Validate first name contains only letters"""
        if value and not re.match(r'^[a-zA-Z]+$', value):
            raise serializers.ValidationError("First name should contain only letters.")
        return value

    def validate_last_name(self, value):
        """Validate last name contains only letters"""
        if value and not re.match(r'^[a-zA-Z]+$', value):
            raise serializers.ValidationError("Last name should contain only letters.")
        return value

    def create(self, validated_data):
        """Create and return a new user"""
        validated_data.pop('password2')
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        help_text="Enter your registered email address"
    )
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        help_text="Enter your password"
    )

    def validate(self, attrs):
        """Validate user credentials"""
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError('Must include "email" and "password".')
            
        normalized_email = normalize_email(email)    

        user = User.objects(email=normalized_email).first()
        if not user:
            raise serializers.ValidationError('Invalid email or password.')
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')
        # if not user.check_password(password):
        #     raise serializers.ValidationError('Must include "email" and "password".')

        # Check password - this is crucial!
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid email or password.')

        attrs['user'] = user
        return attrs

class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True, source='pk')
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)

    def to_representation(self, instance):
        """Convert MongoDB ObjectId to string for JSON serialization"""
        representation = super().to_representation(instance)
        representation['id'] = str(instance.pk)  # Convert ObjectId to string
        return representation
    
    # Custom Token Serializer for SimpleJWT
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get(self.username_field)
        password = attrs.get('password')
        
        if not email or not password:
            raise serializers.ValidationError('Must include "email" and "password".')
        
        # Normalize email
        normalized_email = normalize_email(email)
            
        user = User.objects.filter(email=normalized_email).first()
        if not user:
            raise serializers.ValidationError('Invalid email or password.')
        
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')
        
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid email or password.')
        
        # Set the user for token generation
        self.user = user
        
        # Generate tokens
        refresh = self.get_token(self.user)
        
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': str(user.id),
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        }
        
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['user_id'] = str(user.id)
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        
        return token