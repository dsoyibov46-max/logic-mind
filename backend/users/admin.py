from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        ('Logic Mind', {
            'fields': (
                'role',
                'parent',
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Logic Mind', {
            'fields': (
                'role',
                'parent',
            )
        }),
    )

    list_display = (
        'username',
        'email',
        'role',
        'parent',
        'is_staff',
    )

    list_filter = (
        'role',
        'is_staff',
    )