from pydantic import BaseModel

from movies_auth.app import ma
from movies_auth.app.models import User


class SignUpRequestBody(BaseModel):
    login: str
    password: str


class SignInRequestBody(BaseModel):
    login: str
    password: str


class UserResponse(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ("id", "is_superuser", "login")


class AuthTokensResponse(ma.Schema):
    class Meta:
        model = User
        fields = ("id", "is_superuser", "login")


user_response = UserResponse()
