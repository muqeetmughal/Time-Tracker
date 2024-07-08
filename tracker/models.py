from django.db import models
from django.utils import timezone
from .model_choices import *
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, full_name, password, **extra_fields)

class CustomUser(AbstractUser, PermissionsMixin): 
    full_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to="profile_image")
    time_zone = models.CharField(max_length=6, choices=TimeZoneChoices)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email



class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return super().update(deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def restore(self):
        return self.update(deleted_at=None)
class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    objects = SoftDeleteManager()  
    all_objects = models.Manager()  

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self, using=None, keep_parents=False):
        super().delete(using, keep_parents)

    def restore(self):
        self.deleted_at = None
        self.save()

    @property
    def is_deleted(self):
        return self.deleted_at is not None


class Projects(BaseModel):
    name = models.CharField(max_length=100)
    currency = models.CharField(max_length=1, choices=CurrencyChoices)
    allow_web_tracker = models.BooleanField(default=True)
    allow_desktop_tracker = models.BooleanField(default=True)
    take_screenshots = models.BooleanField(default=True)
    screenshot_interval = models.CharField(max_length=1, choices=ScreenshotInterval)
    count_mouse_clicks = models.BooleanField(default=True)
    count_keyboard_hits = models.BooleanField(default=True)
    manual_time_tracker = models.BooleanField(default=True)
    team = models.ManyToManyField("Team", blank=True)

    def __str__(self) -> str:
        return self.name


class Activity(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.SET_NULL, null=True)
    description = models.TextField( null=True)
    start_date = models.DateField()
    work_from = models.TimeField()
    work_to = models.TimeField()
    type = models.CharField(max_length=1, choices=ActivityType)
    keyboard_event_counts = models.PositiveIntegerField()
    mouse_event_counts = models.PositiveIntegerField()
    # active_window_title = models.CharField(max_length=255)
    screenshot = models.ManyToManyField("ScreenShot", blank=True)
    webcam = models.ManyToManyField("WebCam", blank=True)

    def __str__(self) -> str:
        return self.project.name



class Team(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="customuser")
    is_active = models.BooleanField(default=False)


class ScreenShot(models.Model):
    image = models.ImageField(upload_to="screenshots", blank=True)

class WebCam(models.Model):
    image = models.ImageField(upload_to="webcam_images", blank=True)

