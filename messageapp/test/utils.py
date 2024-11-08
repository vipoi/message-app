import base64
from messageapp.models import Message, UserAccount


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
    return user


def create_test_message(sender: UserAccount, receiver: UserAccount, content: str = "TestMessage"):
    """Creates a new message"""
    message = Message.objects.create(
        sender=sender,
        receiver=receiver,
        content=content
    )
    return message
