from typing import List

from django.db.models import Q
from ninja import Query, Router

from messageapp.api.schemas import CreateMessageSchema, MessageFilterSchema, MessageSchema
from messageapp.auth import BasicAuth
from messageapp.models import Message, UserAccount

router = Router(auth=BasicAuth())


@router.get("/", response=List[MessageSchema])
def list_messages(request, filters: Query[MessageFilterSchema]):
    messages = Message.objects.order_by(
        'deleted_at').filter(deleted_at__isnull=False)

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
