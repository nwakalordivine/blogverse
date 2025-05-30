from rest_framework import generics
from .serializers import RegisterSerializer, UserprofileSerializer, uploadSerializer
from django.contrib.auth.models import User
from .models import Userprofile
from rest_framework.permissions import IsAuthenticated

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class UserprofileDetailAPIView(generics.ListAPIView):
    queryset = Userprofile.objects.all()
    serializer_class = UserprofileSerializer
    lookup_field = 'pk'


class AvatarUpdateAPIViews(generics.UpdateAPIView):
    serializer_class = uploadSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Userprofile.objects.get(user=self.request.user)


class UserMeAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserprofileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Userprofile.objects.get(user=self.request.user)