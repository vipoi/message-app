from django.contrib.auth.models import AbstractUser
from django.db import models


class UserAccount(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)


class Message(models.Model):
    sender = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name='received_messages')
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
