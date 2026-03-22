from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display  = ['email', 'name', 'role', 'city', 'is_verified', 'is_active', 'date_joined']
    list_filter   = ['role', 'is_verified', 'is_active', 'is_staff']
    search_fields = ['email', 'name', 'phone', 'agency']
    ordering      = ['-date_joined']

    fieldsets = (
        (None,            {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'phone', 'city', 'avatar')}),
        ('Role & Agent',  {'fields': ('role', 'agency', 'rera_number', 'experience', 'is_verified')}),
        ('Permissions',   {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone', 'role', 'password1', 'password2'),
        }),
    )
