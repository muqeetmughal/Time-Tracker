from django.contrib import admin
from authentication.models import UserAccount, Profile
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authentication.forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = UserAccount
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        # ('Personal info', {
        #     'fields': ('full_name',)}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "full_name", "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions", "is_superuser"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(UserAccount, CustomUserAdmin)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['user', 'type', 'active']
admin.site.register(Profile,ProfileAdmin)