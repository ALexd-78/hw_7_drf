from rest_framework import generics

from users.models import User
from users.serializers import UserSerializer


class RegisterCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ProfileUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self, queryset=None):
        return self.request.user
