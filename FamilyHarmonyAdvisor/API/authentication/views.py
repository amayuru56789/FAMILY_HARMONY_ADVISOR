from django.shortcuts import render

# Create your views here.
# authentication/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from .models import User
from datetime import datetime

def get_tokens_for_user(user):
    # For MongoEngine, we need to create a user object that Django auth can understand
    # This is a workaround since SimpleJWT expects Django User model
    from django.contrib.auth.models import User as DjangoUser
    
    # Generate JWT tokens for MongoEngine User
    refresh = RefreshToken()
    refresh["user_id"] = str(user.id)
    refresh["email"] = user.email
    refresh['first_name'] = user.first_name
    refresh['last_name'] = user.last_name
    refresh["is_staff"] = user.is_staff
    refresh["is_superuser"] = user.is_superuser
    
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        tokens = get_tokens_for_user(user)
        user_data = UserSerializer(user).data
        
        return Response({
            'user': user_data,
            'tokens': tokens,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        tokens = get_tokens_for_user(user)
        
        # Update last login
        user.last_login = datetime.now()
        user.save()
        
        user_data = UserSerializer(user).data
        
        return Response({
            'user': user_data,
            'tokens': tokens,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
    """
    Get current user profile from MongoDB
    """
    try:

        # Get user ID from token claims (stored during token generation)
        user_id = request.auth.payload.get('user_id')
        
        if not user_id:
            return Response({'error': 'User ID not found in token'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        # For MongoEngine, we need to get the user by email from the token
        user = User.objects.get(id=user_id)
        user_data = UserSerializer(user).data
        return Response(user_data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout user
    """
    try:
        refresh_token = request.data.get('refresh_token')
        if  not refresh_token:
            return Response({'error': 'Refresh token is required'}, 
                    status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refresh_token_view(request):
    """
    Refresh JWT token
    """
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        token = RefreshToken(refresh_token)
        
        # Get user ID from the token to create new tokens
        user_id = token.payload.get('user_id')
        if not user_id:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(id=user_id)
        new_tokens = get_tokens_for_user(user)
        
        return Response(new_tokens, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)