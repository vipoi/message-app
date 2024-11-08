from ninja import ModelSchema, Router, Schema
from pydantic import field_validator, model_validator

from messageapp.api.schemas import AccountSchema
from messageapp.auth import BasicAuth
from messageapp.models import UserAccount

router = Router()


@router.get("/me/", auth=BasicAuth(), response=AccountSchema)
def get_current_account(request):
    """Returns the authenticated user"""
    return request.auth


class CreateAccountSchema(Schema):
    username: str
    password: str
    password_confirm: str

    @model_validator(mode='after')
    def check_unique(self):
        if self.password != self.password_confirm:
            raise ValueError('passwords do not match')
        return self

    @field_validator('username')
    @classmethod
    def check_username_unique(cls, value):
        if UserAccount.objects.filter(username=value).exists():
            raise ValueError("This username is not available")
        return value


@router.post("/", response=AccountSchema)
def create_account(request, data: CreateAccountSchema):
    """Creates a new user"""
    user = UserAccount(username=data.username)
    user.set_password(data.password)
    user.save()
    return user
