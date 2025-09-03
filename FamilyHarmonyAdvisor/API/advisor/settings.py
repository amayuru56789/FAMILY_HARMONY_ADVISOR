# """
# Django settings for advisor project.
# """

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-utb)bauiha07vhe1pc4$@t298*#!z1k&iinj%79k2+#x8(@lyp')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')

# MongoDB Atlas Connection
MONGODB_ATLAS_CLUSTER = os.environ.get(
    'MONGODB_ATLAS_CLUSTER', 
    'mongodb+srv://indeewara5678_db_user:o0uF2qjVFB3JTN1k@cluster0.lkgjgsq.mongodb.net/'
)

# Initialize MongoDB connection
try:
    from mongoengine import connect
    # Connect to MongoDB Atlas
    connect(host=MONGODB_ATLAS_CLUSTER)
    print("✓ MongoDB Atlas connection established successfully!")
except Exception as e:
    print(f"✗ MongoDB Atlas connection failed: {e}")

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    'authentication',
    'familyadvisor', 
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Add this at the top
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'advisor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'advisor.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': MONGODB_ATLAS_CLUSTER,
            'authMechanism': 'SCRAM-SHA-1',
        }
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

# JWT Settings
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Use custom authentication backend
AUTHENTICATION_BACKENDS = [
    'authentication.backends.MongoDBBackend',
]

# Custom user model
AUTH_USER_MODEL = 'authentication.User'

# import mongoengine

# mongoengine.connect(
#     db="FamilyHarmonyDB",
#     host="mongodb+srv://indeewara5678_db_user:o0uF2qjVFB3JTN1k@cluster0.lkgjgsq.mongodb.net/"
# )




"""
Django settings for advisor project.
"""

# import os
# from pathlib import Path
# from dotenv import load_dotenv
# from datetime import timedelta

# # Load environment variables
# load_dotenv()

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

# # Quick-start development settings - unsuitable for production
# SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-utb)bauiha07vhe1pc4$@t298*#!z1k&iinj%79k2+#x8(@lyp')
# DEBUG = os.environ.get('DEBUG', 'True') == 'True'
# ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')

# # MongoDB Atlas Connection
# MONGODB_ATLAS_CLUSTER = os.environ.get(
#     'MONGODB_ATLAS_CLUSTER', 
#     'mongodb+srv://indeewara5678_db_user:o0uF2qjVFB3JTN1k@cluster0.lkgjgsq.mongodb.net/'
# )

# # Initialize MongoDB connection
# try:
#     import mongoengine
#     # Connect to MongoDB Atlas with the database name
#     mongoengine.connect(
#         host=MONGODB_ATLAS_CLUSTER,
#         alias='default',
#         name='FamilyHarmonyDB'  # Specify your database name
#     )
#     print("✓ MongoDB Atlas connection established successfully!")
# except Exception as e:
#     print(f"✗ MongoDB Atlas connection failed: {e}")

# # Application definition
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'rest_framework',
#     'corsheaders',
#     'rest_framework_simplejwt',
#     'authentication',
#     'familyadvisor', 
# ]

# MIDDLEWARE = [
#     'corsheaders.middleware.CorsMiddleware',  # Add this at the top
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'advisor.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'advisor.wsgi.application'

# # Since we're using MongoDB, we don't need the SQL database configuration
# # Remove the DATABASES section entirely if using only MongoDB
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.dummy',  # Use dummy backend for MongoDB
#     }
# }

# # Password validation
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

# # Internationalization
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_TZ = True

# # Static files
# STATIC_URL = 'static/'

# # Default primary key field type
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # CORS settings
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
# ]

# # REST Framework settings
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ),
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.AllowAny',
#     ),
# }

# # JWT Settings
# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
#     'ROTATE_REFRESH_TOKENS': True,
#     'BLACKLIST_AFTER_ROTATION': True,
# }

# # Use custom authentication backend
# AUTHENTICATION_BACKENDS = [
#     'authentication.backends.MongoDBBackend',
# ]

# # Custom user model
# AUTH_USER_MODEL = 'authentication.User'