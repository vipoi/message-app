from ninja import ModelSchema, Router, Schema
from pydantic import field_validator, model_validator
from messageapp.auth import BasicAuth
from messageapp.models import UserAccount

router = Router()


class UserSchema(ModelSchema):
    class Meta:
        model = UserAccount
        fields = ['username', 'created_at', 'deleted_at']


@router.get("/me/", auth=BasicAuth(), response=UserSchema)
def get_current_account(request):
    return request.auth


class SignupSchema(Schema):
    username: str
    password: str
    password_confirm: str

    @model_validator(mode='after')
    def check_unique(self):
        pw1 = self.password
        pw2 = self.password_confirm
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('passwords do not match')
        return self

    @field_validator('username')
    @classmethod
    def check_username_unique(cls, value):
        if UserAccount.objects.filter(username=value).exists():
            raise ValueError("This username is not available")
        return value


@router.post("/", response=UserSchema)
def create_account(request, data: SignupSchema):
    user = UserAccount(username=data.username)
    user.set_password(data.password)
    user.save()
    return user
