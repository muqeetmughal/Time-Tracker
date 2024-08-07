from django.contrib import admin
from .models import *

class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ['name','currency','created_by']

admin.site.register(Project, ProjectAdmin)
class ActivityAdmin(admin.ModelAdmin):
    model = Activity
    list_display = ['member','project','type']

admin.site.register(Activity, ActivityAdmin)
admin.site.register(Shot)
class MemberAdmin(admin.ModelAdmin):
    model = Membership
    list_display = ['project','profile','role', 'is_active']
admin.site.register(Membership, MemberAdmin)