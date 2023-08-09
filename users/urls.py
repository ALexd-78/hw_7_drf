from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterCreateAPIView, ProfileUpdateAPIView

app_name = UsersConfig.name

urlpatterns = [
path('register/', RegisterCreateAPIView.as_view(), name='register'),
path('profile/', ProfileUpdateAPIView.as_view(), name='profile'),

]