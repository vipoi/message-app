import base64
from django.test import Client
from messageapp.models import UserAccount


def basic_auth_header(username: str, password: str):
    """Returns a dict with a basic auth authorization header"""
    credentials = f'{username}:{password}'.encode()
    encoded_credentials = base64.b64encode(credentials).decode()
    return {
        'Authorization': f'Basic {encoded_credentials}'
    }


def create_test_user(username: str, password: str):
    """Creates a new user and sets its password"""
    user = UserAccount.objects.create(
        username=username
    )
    user.set_password(password)
    user.save()
