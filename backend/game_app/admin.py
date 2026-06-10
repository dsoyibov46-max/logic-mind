from django.contrib import admin
from .models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'url_name',
        'is_active',
        'created_at',
    )

    list_filter = (
        'is_active',
        'created_at',
    )

    search_fields = (
        'title',
        'description',
        'url_name',
    )

    list_editable = (
        'is_active',
    )

    readonly_fields = (
        'created_at',
    )