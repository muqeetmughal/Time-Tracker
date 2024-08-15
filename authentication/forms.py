import email
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from authentication.models import UserAccount
from tracker.models import Organization
from django import forms

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = UserAccount
        fields = [
            'email',
            # 'role',
            'full_name',
            'country',
            'city',
            'time_zone',
            'password1',  # Password1 is required for UserCreationForm
            'password2',  # Password2 is for password confirmation
        ]
        
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Create an Organization for the new user
            Organization.objects.create(owner=user, name=user.email)
        return user
 

        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UserAccount
        fields = ('email', 'role', 'full_name', 'country', 'city', 'time_zone')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = self.instance

        if email and UserAccount.objects.filter(email=email).exclude(pk=user.pk).exists():
            raise forms.ValidationError("A user with that email already exists.")

        return email
        
        
             





# class CustomUserChangeForm(UserChangeForm):

#     class Meta:
#         model = UserAccount
#         fields = ("email", )