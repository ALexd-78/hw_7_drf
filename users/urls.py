from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import RegisterCreateAPIView, ProfileUpdateAPIView

app_name = UsersConfig.name

urlpatterns = [
path('register/', RegisterCreateAPIView.as_view(), name='register'),
path('profile/', ProfileUpdateAPIView.as_view(), name='profile'),
path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]