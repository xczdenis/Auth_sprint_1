from uuid import UUID

from marshmallow import Schema, fields
from pydantic import BaseModel, Extra

from movies_auth.app import ma
from movies_auth.app.common.enums import ConditionsEnum
from movies_auth.app.models import Permission, User


class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str


class UserPermissionsUpdate(BaseModel):
    user_id: UUID
    permissions: list[str]

    class Config:
        extra = Extra.forbid


class PermissionsUpdate(BaseModel):
    data: list[UserPermissionsUpdate]

    class Config:
        extra = Extra.forbid


class HasPermRequest(BaseModel):
    permissions: list[str]
    condition: ConditionsEnum = ConditionsEnum.AND

    class Config:
        extra = Extra.forbid


class AccessLogItemResponse(Schema):
    user_agent = fields.Str()
    created = fields.DateTime()
    device_type = fields.Str()


class PermissionDetailResponse(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Permission


class UserDetailResponse(ma.SQLAlchemyAutoSchema):
    permissions = fields.Nested(PermissionDetailResponse(), many=True)

    class Meta:
        model = User
        exclude = ("password",)


class UserListItemResponse(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "login", "email", "is_superuser")


access_log_item_response = AccessLogItemResponse()
user_list_item_response = UserListItemResponse()
user_detail_response = UserDetailResponse()
