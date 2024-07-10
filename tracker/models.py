from django.db import models
from django.utils import timezone
from .model_choices import *
from authentication.models import UserAccount

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


class Project(BaseModel):
    user = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    currency = models.CharField(max_length=1, choices=CurrencyChoices, default=CurrencyChoices.USD)
    allow_web_tracker = models.BooleanField(default=True)
    allow_desktop_tracker = models.BooleanField(default=True)
    take_screenshots = models.BooleanField(default=True)
    screenshot_interval = models.CharField(max_length=1, choices=ScreenshotInterval.choices, default=ScreenshotInterval.FIVE_MINUTES)
    count_mouse_clicks = models.BooleanField(default=True)
    count_keyboard_hits = models.BooleanField(default=True)
    manual_time_tracker = models.BooleanField(default=True)
    # team = models.ManyToManyField("Team", blank=True)

    def __str__(self) -> str:
        return self.name


class Activity(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    work_from = models.TimeField()
    work_to = models.TimeField()
    type = models.CharField(max_length=1, choices=ActivityType)
    keyboard_event_counts = models.PositiveIntegerField()
    mouse_event_counts = models.PositiveIntegerField()
    # active_window_title = models.CharField(max_length=255)
    artifacts = models.ManyToManyField("Artifact", blank=True)

    # def __str__(self) -> str:
    #     return self



class Member(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT, null=True, blank=True, related_name="members")
    # user can not be deleted if user is linked as team member in any project
    user = models.ForeignKey(UserAccount, on_delete=models.PROTECT, null=True, related_name="memberships")
    role = models.CharField(max_length=1, choices=RoleChoices.choices, default=RoleChoices.WORKER)
    invitation_accepted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.email


class Artifact(models.Model):
    image = models.ImageField(upload_to="artifacts", blank=True)
    type = models.CharField(max_length=1, choices=ArtifactTypeChoices.choices, default=ArtifactTypeChoices.SCREENSHOT)


