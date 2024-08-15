from django.contrib import admin
from .models import *


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'owner', 'created_at')
    search_fields = ('name', 'owner__email')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    
    
class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ['name','created_at']

admin.site.register(Project, ProjectAdmin)



@admin.register(OrganizationMembership)
class OrganizationMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'is_admin')
    search_fields = ('user__email', 'organization__name')
    list_filter = ('is_admin',)
    
    
    
# class ActivityAdmin(admin.ModelAdmin):
#     model = Activity
#     list_display = ['member','project','type']

# admin.site.register(Activity, ActivityAdmin)
# admin.site.register(Shot)
# class MemberAdmin(admin.ModelAdmin):
#     model = Membership
#     list_display = ['project','profile','role', 'is_active']
# admin.site.register(Membership, MemberAdmin)