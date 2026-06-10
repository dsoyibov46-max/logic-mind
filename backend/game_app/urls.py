from django.urls import path
from . import views

app_name = 'game_app'

urlpatterns = [

    path('', views.games_list, name='games_list'),

    path('router/<slug:slug>/', views.game_router, name='game_router'),

    path('electro-labirint/', views.electro_labirint_view, name='labirint'),

    path('memory/', views.memory_game_view, name='memory'),

    path('math/', views.math_game_view, name='math'),  # ← qo'shildi

]