from rest_framework import serializers
from tracker.models import *
from authentication.models import UserAccount
# from authentication.serializers import ProfileSerializer
# class MemberSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Membership
#         fields = "__all__"


# class ProjectSerializer(serializers.ModelSerializer):
#     created_by_name = serializers.ReadOnlyField()
#     created_by_user_email = serializers.ReadOnlyField()
#     project_role = serializers.ReadOnlyField()
#     members_count = serializers.ReadOnlyField()
    
#     engagements = MemberSerializer(many=True, read_only=True)
#     class Meta:
#         model = Project
#         fields = "__all__"
#         read_only_fields = [
#             "id",
#             "created_by",
#             "currency",
#             "screenshot_intereval",
#             "allow_web_tracker",
#             "allow_desktop_tracker",
#             "manual_time",
#             "mouse",
#             "keyboard",
#             "screenshot_interval",
#             "take_screenshots",
#             "archived_at",
#             "members_count"
#             # "admin_profile"
#         ]
        
#         # depth = 1


# class ActivitySerializer(serializers.ModelSerializer):
#     project_name = serializers.ReadOnlyField()

#     class Meta:
#         model = Activity
#         exclude = [ "shots"]
#         read_only_fields = ["id","member",]

#     def validate(self, attrs):
#         return super().validate(attrs)

    # def create(self, validated_data):
    #     # Override create method to handle single instance or list
    #     if isinstance(validated_data, list):
    #         return [Activity.objects.create(**item) for item in validated_data]
    #     else:
    #         return Activity.objects.create(**validated_data)


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = [
            "id",
            "full_name",
            "email",
            "country",
            "city",
            "image",
            "time_zone",
            "password",
        ]



# class UserLoginSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(max_length=255)

#     class Meta:
#         model = UserAccount
#         fields = ['email', 'password']


# class ShotSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Shot
#         fields = "__all__"
