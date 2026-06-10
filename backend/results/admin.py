from django.contrib import admin
from .models import GameResult


@admin.register(GameResult)
class GameResultAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'game',
        'score',
        'time_spent',
        'level_reached',
        'played_at',
    )
    list_filter = ('game', 'played_at')
    search_fields = ('user__username', 'game__title')
    ordering = ('-played_at',)