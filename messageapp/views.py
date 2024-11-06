from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets

from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

from messageapp.serializers import SignupSerializer


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = SignupSerializer
