from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from tracker.model_choices import TimeZoneChoices
from django.utils.translation import gettext_lazy as _
from authentication.managers import CustomUserManager
from django.core.validators import EmailValidator
from django.conf import settings
from datetime import datetime
from common.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F


UserAccount = settings.AUTH_USER_MODEL

email_validator = EmailValidator(message="%(value)s is not a valid email address.")

class UserAccount(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_("Email address"), unique=True, 
        error_messages={
            'unique': 'This Email is already registered. Please choose a different one.',
            'max_length': 'This Email is %(show_value)s characters long. The maximum allowed length is %(limit_value)s.',
            "required": "This Field is required!"
        },)

    # -----additional added
    # phone = models.CharField(max_length=20)
    # allow_web_login = models.BooleanField(default=True)
    full_name = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    time_zone = models.CharField(max_length=6, choices=TimeZoneChoices.choices)
    # -----additional added
    # is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    # Call the validate_email function with a custom message
    def clean(self):
        email_validator(self.email)

class Profile(BaseModel):
    USER_TYPES = (
        ("freelancer", "Freelancer"),
        ("client", "Client"),
    )
    
    image = models.ImageField(upload_to="profile_images",null=True, blank=True)
    
    name = models.CharField(max_length=255,null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="profiles")
    type = models.CharField(max_length=10, choices=USER_TYPES)
    active = models.BooleanField(default=False)
    class Meta:
        unique_together = ("user", "type")

    def __str__(self):
        return f"{self.user.email} ({self.get_type_display()})"
    
    
@receiver(post_save, sender=Profile)
def ensure_single_active_profile(sender, instance, created, **kwargs):
    if instance.active or not instance.active:
        Profile.objects.filter(user=instance.user).exclude(pk=instance.pk).update(active=~F('active'))