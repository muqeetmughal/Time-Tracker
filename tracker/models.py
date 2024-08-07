from django.db import models
from django.utils import timezone
from authentication.models import UserAccount
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


class Project(BaseModel):
    name = models.CharField(max_length=100)
    currency = models.CharField(
        max_length=3, choices=CurrencyChoices.choices, default=CurrencyChoices.USD
    )

    allow_web_tracker = models.BooleanField(default=True)
    allow_desktop_tracker = models.BooleanField(default=True)
    take_screenshots = models.BooleanField(default=True)
    screenshot_interval = models.PositiveIntegerField(
        default=30,
    )
    mouse = models.BooleanField(default=True)
    keyboard = models.BooleanField(default=True)
    manual_time = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        "authentication.Profile",
        on_delete=models.CASCADE,
        related_name="created_projects",
    )


    def __str__(self) -> str:
        return self.name


class Membership(BaseModel):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, null=True, blank=True, related_name="engagements"
    )
    profile = models.ForeignKey(
        "authentication.Profile",
        on_delete=models.PROTECT,
        null=True,
        related_name="team_engagements",
    )
    role = models.CharField(
        max_length=10, choices=RoleChoices.choices, default=RoleChoices.WORKER
    )
    is_active = models.BooleanField(default=False)
    class Meta:
        
        unique_together = ('project', 'profile')
    def __str__(self) -> str:

        return f"Membership: {self.profile.user.email} of {self.project}"


class Invitation(BaseModel):
       
    token = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    message = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=50, choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')),default='pending')
    user = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(default=timezone.now)
    sent_by = models.ForeignKey(
        "authentication.Profile",
        on_delete=models.CASCADE,
        related_name="sent_invitations",
    )
    role = models.CharField(
        max_length=10, choices=RoleChoices.choices, default=RoleChoices.WORKER
    )
    ### if client wants to invite a user on specfic rate
    rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"Invitation to {self.email} for {self.project.name}"

# class Engagement(BaseModel):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     member = models.ForeignKey(Membership, on_delete=models.CASCADE)

class Activity(BaseModel):
    member = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    description = models.TextField(blank=True, null=True)
    # start_date = models.DateField()
    work_from = models.DateTimeField()
    work_to = models.DateTimeField()
    type = models.CharField(max_length=1, choices=ActivityType.choices)
    keyboard_event_counts = models.PositiveIntegerField(default=0, blank=True)
    mouse_event_counts = models.PositiveIntegerField(default=0, blank=True)
    shots = models.ManyToManyField("Shot", blank=True)

    # def __str__(self) -> str:
    #     return f"Activity by {self.user.user.user.email} on {self.project.name}"


class Shot(BaseModel):
    image = models.ImageField(upload_to="shots",null=True, blank=False, default=None)
    type = models.CharField(
        max_length=1,
        choices=ShotTypeChoices.choices,
        default=ShotTypeChoices.SCREENSHOT,
    )
    associated_shot = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    blurred = models.BooleanField(default=False)
    is_time_randomized = models.BooleanField(default=False)
    taken_at = models.DateTimeField(default=timezone.now)
    

    def __str__(self) -> str:
        return f"Shot {self.image} ({self.get_type_display()})"


@receiver(post_save, sender=Project)
def create_member_for_project(sender, instance, created, **kwargs):
    if created:
        
        # Assuming the creator of the project is the initial member
        Membership.objects.create(
            project=instance,
            profile=instance.created_by,
            role=RoleChoices.ADMIN,
            is_active=True,
        )
