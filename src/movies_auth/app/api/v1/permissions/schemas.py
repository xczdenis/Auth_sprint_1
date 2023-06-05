from pydantic import BaseModel, Extra

from movies_auth.app import ma
from movies_auth.app.models import Permission


class PermissionCreate(BaseModel):
    codename: str
    name: str


class PermissionUpdate(BaseModel):
    codename: str | None
    name: str | None

    class Config:
        extra = Extra.forbid


class PermissionResponse(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Permission
        fields = ("id", "codename", "name")


permission_response = PermissionResponse()
