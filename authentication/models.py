from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from authentication.managers import CustomUserManager
from django.core.validators import EmailValidator
from django.conf import settings
from datetime import datetime


UserAccount = settings.AUTH_USER_MODEL

email_validator = EmailValidator(message="%(value)s is not a valid email address.")

class UserAccount(AbstractBaseUser, PermissionsMixin):

    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(_("Email address"), unique=True, 
        error_messages={
            'unique': 'This Email is already registered. Please choose a different one.',
            'max_length': 'This Email is %(show_value)s characters long. The maximum allowed length is %(limit_value)s.',
            "required": "This Field is required!"
        },)

    # -----additional added
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to="profile_images", null=True)
   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # -----additional added
    # is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    # Call the validate_email function with a custom message
    def clean(self):
        email_validator(self.email)
