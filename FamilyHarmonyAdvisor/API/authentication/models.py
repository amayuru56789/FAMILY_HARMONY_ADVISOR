from django.db import models

# Create your models here.

# authentication/models.py
# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from django.contrib.auth.hashers import make_password, check_password
# import re
# from django.core.exceptions import ValidationError

# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(email, password, **extra_fields)

# class User(AbstractBaseUser):

#       # Add ObjectIdField for MongoDB compatibility
#     id = models.ObjectIdField(primary_key=True)

#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=50, blank=True)
#     last_name = models.CharField(max_length=50, blank=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     last_login = models.DateTimeField(auto_now=True)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     class Meta:
#         # Optional: specify collection name
#         db_table = 'Family_Conflict'

#     def __str__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         return self.is_superuser

#     def has_module_perms(self, app_label):
#         return self.is_superuser

#     def set_password(self, raw_password):
#         self.password = make_password(raw_password)

#     def check_password(self, raw_password):
#         return check_password(raw_password, self.password)

#     def clean(self):
#         if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.email):
#             raise ValidationError('Invalid email format')

# Alternative approach without ObjectIdField
# from django.db import models  # Keep using django.db.models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from django.contrib.auth.hashers import make_password, check_password
# import re
# from django.core.exceptions import ValidationError

# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(email, password, **extra_fields)

# class User(AbstractBaseUser):
#     # Remove the explicit id field or use AutoField
#     # Django will automatically create an id field
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=50, blank=True)
#     last_name = models.CharField(max_length=50, blank=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     last_login = models.DateTimeField(auto_now=True)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     def __str__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         return self.is_superuser

#     def has_module_perms(self, app_label):
#         return self.is_superuser

#     def set_password(self, raw_password):
#         self.password = make_password(raw_password)

#     def check_password(self, raw_password):
#         return check_password(raw_password, self.password)

#     def clean(self):
#         if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.email):
#             raise ValidationError('Invalid email format')

# authentication/models.py

from django.contrib.auth.hashers import make_password, check_password
import re
from django.core.exceptions import ValidationError
import mongoengine as me

class UserManager():
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = User(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
    @staticmethod
    def normalize_email(email):
        """
        Lowercases the domain part of the email address.
        """
        return email.strip().lower()

class User():
    _id = me.ObjectIdField()
    email = me.EmailField(unique=True)
    first_name = me.StringField(max_length=50, blank=True)
    last_name = me.StringField(max_length=50, blank=True)
    is_active = me.BooleanField(default=True)
    is_staff = me.BooleanField(default=False)
    is_superuser = me.BooleanField(default=False)
    date_joined = me.DateTimeField(auto_now_add=True)
    last_login = me.DateTimeField(auto_now=True)

    meta = {
        "collection": "Family_Conflict"
    }

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'auth_users'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def clean(self):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.email):
            raise ValidationError('Invalid email format')
