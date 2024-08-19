from django import forms
from .models import OrganizationMembership, Project, Organization


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