import email
from enum import unique
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from authentication.models import UserAccount
from django.db import transaction
from tracker.models import Organization
from django import forms

class SignupForm(UserCreationForm):
    # orgnization_name = forms.CharField(max_length=50, required=True)
    class Meta:
        model = UserAccount
        fields = [
            'email',
            # 'role',
            'full_name',
            'country',
            'city',
            'time_zone',
            'password1', 
            'password2', 
        ]
    
        
    # def save(self, commit=True):
    #     with transaction.atomic():
    #         user = super().save(commit=False)
    #         if commit:
    #             user.save()
    #             Organization.objects.create(owner=user, name=orgnization_name)
    #         return user
    
        

        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UserAccount
        fields = ('email', 'full_name', 'country', 'city', 'time_zone')

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