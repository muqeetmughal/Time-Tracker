from django import forms
from .models import OrganizationMembership, Project, Organization, ProjectMember
from authentication.models import *


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name']  



class OrganizationMembershipForm(forms.ModelForm):
    class Meta:
        model = OrganizationMembership
        fields = ['user', 'organization', 'is_admin']



class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'organization', 'description']
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['organization'].queryset = Organization.objects.filter(members=user)
            print("Filtered organizations:", self.fields['organization'].queryset)

            
# class AddMembersForm(forms.Form):
    
#     users = forms.ModelMultipleChoiceField(
#         queryset=UserAccount.objects.filter(is_superuser= False),
#         widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
#         label="Select Users"
#     )

class AddMembersForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        queryset=UserAccount.objects.filter(is_superuser=False),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label="Select Users"
    )
    
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        
        if self.project:
            existing_members = ProjectMember.objects.filter(project=self.project).values_list('user_id', flat=True)
            self.fields['users'].widget.choices = [
                (user.id, f"{user} {'(Already Member)' if user.id in existing_members else ''}")
                for user in self.fields['users'].queryset
            ]