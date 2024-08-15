from django.db import models
from django.utils import timezone

from authentication.models import UserAccount#, Organization
from .model_choices import (
    CurrencyChoices,
    ScreenshotInterval,
    ActivityType,
    RoleChoices,
    ShotTypeChoices,
)
from common.models import BaseModel
from django.dispatch import receiver
from django.db.models.signals import post_save


class Organization(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(UserAccount, related_name='owned_organizations', on_delete=models.CASCADE)
    members = models.ManyToManyField(UserAccount, related_name='organizations', through='tracker.OrganizationMembership')

    def __str__(self):
        return self.name


class OrganizationMembership(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)  # Is this user an admin in this organization?



class Project(models.Model):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
