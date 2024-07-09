from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from authentication.models import UserAccount


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = UserAccount
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = UserAccount
        fields = ("email", )