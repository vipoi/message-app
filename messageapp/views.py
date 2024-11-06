from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from messageapp.models import Message
from messageapp.serializers import MessageSerializer, SignupSerializer


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = SignupSerializer


class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        )

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
