from django.urls import path
from .views import save_game_result
from .views import save_game_result, leaderboard

urlpatterns = [
    path('save/', save_game_result, name='save_game_result'),
    path('leaderboard/', leaderboard, name='leaderboard'),
]
