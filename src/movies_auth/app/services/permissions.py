from dataclasses import dataclass

from movies_auth.app import db
from movies_auth.app.common.decorators import trace
from movies_auth.app.common.exceptions import EntityAlreadyExists, EntityDoesntExists
from movies_auth.app.models import Permission


@dataclass(slots=True)
class PermissionService:
    def create_permission(self, name: str, codename: str) -> Permission:
        if self.get_permission_by_name(name) is not None:
            raise EntityAlreadyExists("Permission with name '{name}' already exists".format(name=name))
        if self.get_permission_by_codename(codename) is not None:
            raise EntityAlreadyExists(
                "Permission with codename '{codename}' already exists".format(codename=codename)
            )

        new_permission = Permission()
        new_permission.name = name
        new_permission.codename = codename

        db.session.add(new_permission)
        db.session.commit()

        return new_permission

    def delete_permission_by_id(self, permission_id):
        permission = self.get_permission_by_id(permission_id)
        if permission is None:
            raise EntityDoesntExists("Permission not found")

        db.session.delete(permission)
        db.session.commit()

    def get_permission_by_name(self, name: str) -> Permission | None:
        return Permission.query.filter_by(name=name).first()

    def get_permission_by_codename(self, codename: str) -> Permission | None:
        return Permission.query.filter_by(codename=codename).first()

    def get_permission_by_id(self, permission_id) -> Permission | None:
        return Permission.query.filter_by(id=permission_id).first()

    def update_permission_by_id(self, permission_id, **kwargs):
        permission = self.get_permission_by_id(permission_id)
        if permission is None:
            raise EntityDoesntExists("Permission not found")

        name = kwargs.get("name")
        codename = kwargs.get("codename")

        query = db.session.query(Permission).filter(Permission.id != permission_id)
        error_message = ""
        if name is not None and codename is not None:
            query = query.filter((Permission.name == name) | (Permission.codename == codename))
            error_message = "Permission with name '{name}' or codename '{codename}' already exists".format(
                name=name, codename=codename
            )
        elif name is not None:
            query = query.filter(Permission.name == name)
            error_message = "Permission with name '{name}' already exists".format(name=name)
        elif codename is not None:
            query = query.filter(Permission.codename == codename)
            error_message = "Permission with codename '{codename}' already exists".format(codename=codename)

        if query.first():
            raise EntityAlreadyExists(error_message)

        for field, value in kwargs.items():
            if value is not None and hasattr(permission, field) and value != getattr(permission, field):
                setattr(permission, field, value)

        db.session.commit()

        return permission

    @trace()
    def get_permissions_by_codenames(self, codenames: list[str]):
        return db.session.query(Permission).filter(Permission.codename.in_(codenames)).all()
