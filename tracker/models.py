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



class NonDeleted(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = False)
    
class SoftDelete(models.Model):
    is_deleted = models.BooleanField(default=False)
    
    objects = NonDeleted()
    all_objects = models.Manager() 
    
    def soft_delete(self):
        self.is_deleted = True 
        self.save()
        
    def restore(self):
        self.is_deleted = False
        self.save()
    
    class Meta:
        abstract = True
        
        

    


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



class Project(SoftDelete):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().save(*args, **kwargs)
        if user:
            ProjectMember.objects.get_or_create(user=user, project=self)
    


class ProjectMember(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return f"{self.user.email} is a member of {self.project.name}"