from django.urls import path
from .views import RegisterAPIView, ProfileAPIView

urlpatterns = [
    path('api/users/register/', RegisterAPIView.as_view(), name='api_register'),
    path('me/', ProfileAPIView.as_view(), name='profile'),
]