from rest_framework import serializers
from .models import * 

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        # fields = "__all__"
        exclude = ["deleted_at"]

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = "__all__"

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "full_name", "email", "country", "city", "profile_picture", "time_zone", "password"]

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']