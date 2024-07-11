from rest_framework import serializers
from authentication.models import UserAccount
from authentication.models import Profile

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'email', 'full_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = UserAccount(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    user = UserAccountSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'type']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserAccountSerializer.create(UserAccountSerializer(), validated_data=user_data)
        profile = Profile.objects.create(user=user, **validated_data)
        return profile



class CreateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'type']  # Add more fields as needed

    def create(self, validated_data):
        user = self.context['request'].user  # Fetch the current authenticated user
        profile = Profile.objects.create(user=user, **validated_data)
        return profile
