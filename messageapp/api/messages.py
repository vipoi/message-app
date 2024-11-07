from typing import List

from django.db.models import Q
from ninja import Field, ModelSchema, Query, Router, Schema
from pydantic import field_validator

from messageapp.auth import BasicAuth
from messageapp.models import Message, UserAccount

router = Router(auth=BasicAuth())


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
        fields = ['content', 'created_at']


class Filters(Schema):
    limit: int = 100
    offset: int = None
    username: str = None


@router.get("/", response=List[MessageSchema])
def list_messages(request, filters: Query[Filters]):
    messages = Message.objects.order_by('created_at')

    if filters.username is None:
        messages = messages.filter(
            Q(sender=request.auth) | Q(receiver=request.auth)
        )
    else:
        messages = messages.filter(
            (Q(sender__username=filters.username) & Q(receiver=request.auth))
            | (Q(sender=request.auth) & Q(receiver__username=filters.username))
        )

    if filters.limit is not None and filters.offset is not None:
        messages = messages[filters.offset:filters.offset+filters.limit]

    return messages


@router.post("/", response=MessageSchema)
def create_message(request, data: CreateMessageSchema):
    receiver = UserAccount.objects.get(username=data.receiver)
    message = Message.objects.create(
        content=data.content,
        receiver=receiver,
        sender=request.auth
    )
    message.save()

    return message
