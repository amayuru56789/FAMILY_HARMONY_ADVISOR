from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from mongoengine import connection
import datetime
# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
def test_mongodb_connection(request):
    """Test endpoint to check MongoDB Atlas connection"""
    try:
        # Get the default connection
        conn = connection.get_connection()
        
        # List all databases
        database_names = conn.list_database_names()
        
        return Response({
            'status': 'success',
            'message': 'MongoDB Atlas connection successful',
            'database_names': database_names,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'MongoDB connection failed: {str(e)}'
        }, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint"""
    try:
        conn = connection.get_connection()
        # Try a simple command to test connection
        conn.admin.command('ping')
        
        return Response({
            'status': 'healthy',
            'mongodb': 'connected',
            'timestamp': datetime.datetime.now().isoformat()
        })
    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'mongodb': 'disconnected',
            'error': str(e),
            'timestamp': datetime.datetime.now().isoformat()
        }, status=500)