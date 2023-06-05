import uuid

from faker.providers import BaseProvider

from movies_auth.app.models import Permission
from tests.utils.helpers import add_test_prefix

_permissions_names = ("all", "sport", "series", "adult", "new-movies")
permissions_names = [add_test_prefix(name) for name in _permissions_names]


class PermissionProvider(BaseProvider):
    def permission_name(self) -> str:
        return self.random_element(permissions_names)

    def permission_codename(self) -> str:
        return self.random_element(permissions_names)

    def permission_id(self) -> str:
        return str(uuid.uuid4())

    def permissions(self) -> list[Permission]:
        return [self.permission(name, name) for name in permissions_names]

    def permission(self, name: str = "", codename: str = "") -> Permission:
        permission_name = self.permission_codename()

        permission = Permission()
        permission.id = self.permission_id()
        permission.name = name or permission_name
        permission.codename = codename or permission_name

        return permission
