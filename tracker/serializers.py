from rest_framework import serializers
from tracker.models import * 
from authentication.models import UserAccount

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "currency", "screenshot_intereval"]
        read_only_fields = ['id', 'user'] 

class ActivitySerializer(serializers.ModelSerializer):
    project_name = serializers.ReadOnlyField()
    class Meta:
        model = Activity
        exclude = ["user"]
        read_only_fields = ['id', 'user'] 

    def create(self, validated_data):
        # Override create method to handle single instance or list
        if isinstance(validated_data, list):
            return [Activity.objects.create(**item) for item in validated_data]
        else:
            return Activity.objects.create(**validated_data)
    


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ["id", "full_name", "email", "country", "city", "image", "time_zone", "password"]

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"


# class UserLoginSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(max_length=255)

#     class Meta:
#         model = UserAccount
#         fields = ['email', 'password']

class ArtifactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artifact
        fields = "__all__"