from django.utils import timezone
from typing import List

from django.db.models import Q
from ninja import Query, Router

from messageapp.api.schemas import CreateMessageSchema, MessageFilterSchema, MessageSchema, NotFoundSchema
from messageapp.auth import BasicAuth
from messageapp.models import Message, UserAccount

router = Router(auth=BasicAuth())


@router.get("/", response=List[MessageSchema])
def list_messages(request, filters: Query[MessageFilterSchema]):
    messages = Message.objects.order_by(
        'created_at').filter(deleted_at__isnull=True)

    if filters.username is None:
        messages = messages.filter(
            Q(sender=request.auth) | Q(receiver=request.auth)
        )
    else:
        messages = messages.filter(
            (Q(sender__username=filters.username) & Q(receiver=request.auth))
            | (Q(sender=request.auth) & Q(receiver__username=filters.username))
        )

    if filters.only_unread:
        messages = messages.filter(read_at=None)

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


@router.delete("/{message_id}", response={204: None, 404: NotFoundSchema})
def delete_message(request, message_id: int):
    count, _ = Message.objects.filter(
        id=message_id,
        sender=request.auth
    ).delete()

    if count == 0:
        return 404, None

    return 204, None


@router.patch("/{message_id}/mark_as_read", response={204: None, 404: NotFoundSchema})
def mark_as_read(request, message_id: int):
    count = Message.objects.filter(
        id=message_id,
        receiver=request.auth
    ).update(read_at=timezone.now())

    if count == 0:
        return 404, None

    return 204, None
