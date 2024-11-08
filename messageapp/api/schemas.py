from ninja import Field, ModelSchema, Schema
from pydantic import field_validator

from messageapp.models import Message, UserAccount


class AccountSchema(ModelSchema):
    class Meta:
        model = UserAccount
        fields = ['username', 'created_at']


class CreateMessageSchema(Schema):
    receiver: str
    content: str

    @field_validator('receiver')
    @classmethod
    def check_user_exist(cls, value):
        if not UserAccount.objects.filter(username=value).exists():
            raise ValueError("User does not exist")
        return value


class MessageSchema(ModelSchema):
    sender: str = Field(None, alias="sender.username")
    receiver: str = Field(None, alias="receiver.username")

    class Meta:
        model = Message
        fields = ['id', 'content', 'read_at', 'created_at']


class MessageFilterSchema(Schema):
    limit: int = 100
    offset: int = 0
    username: str = None
    only_unread: bool = False


class NotFoundSchema(Schema):
    detail: str = "Not Found"
