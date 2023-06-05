from dataclasses import dataclass
from typing import Any

from flask_jwt_extended import get_jwt_identity

from movies_auth.app import db
from movies_auth.app.common.decorators import trace
from movies_auth.app.common.enums import AuthenticationMethods, ConditionsEnum
from movies_auth.app.common.exceptions import (
    AuthenticationError,
    EntityAlreadyExists,
    EntityDoesntExists,
    OldPasswordIsIncorrect,
)
from movies_auth.app.common.types import Tokens
from movies_auth.app.common.utils import obtain_auth_tokens
from movies_auth.app.models import Permission, User


@dataclass(slots=True)
class UserService:
    def create_user(self, login: str, password: str) -> User:
        if self.get_user_by_login(login) is not None:
            raise EntityAlreadyExists("The user with the provided login already exists")

        new_user = User()
        new_user.login = login
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return new_user

    def get_user_by_login(self, login: str) -> User | None:
        return User.query.filter_by(login=login).first()

    def signin(self, method: AuthenticationMethods, login: str, password: str, **kwargs) -> tuple[User, Any]:
        user, data = None, None
        if method == AuthenticationMethods.jwt:
            user, data = self.jwt_signin(login, password)
        else:
            raise AuthenticationError("Unknown authentication method")
        if isinstance(user, User) and data is not None:
            user.log_entry(**kwargs)
            return user, data
        raise AuthenticationError("Failed authentication attempt")

    def jwt_signin(self, login: str, password: str) -> tuple[User, Tokens]:
        user = self.get_user_by_credentials(login, password)
        return user, obtain_auth_tokens(user.id, user.is_superuser)

    def get_user_by_credentials(self, login: str, password: str) -> User:
        user = self.get_user_by_login(login)
        if not user or not user.check_password(raw_password=password):
            raise AuthenticationError("Login or password is incorrect")
        return user

    def find_user_by_id(self, user_id) -> User:
        return User.query.filter_by(id=user_id).first()

    @trace()
    def get_user_by_id(self, user_id) -> User:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise EntityDoesntExists("User with id '{user_id}' not found".format(user_id=user_id))
        return user

    def get_user_from_jwt(self) -> User:
        identity = get_jwt_identity()
        user = self.find_user_by_id(identity)
        if not user:
            raise AuthenticationError("Token is incorrect")
        return user

    def change_password(self, user: User, old_password, new_password):
        if not user.check_password(raw_password=old_password):
            raise OldPasswordIsIncorrect("Old password is incorrect")

        user.set_password(new_password)

        db.session.commit()

    @trace()
    def add_user_permissions(self, user: User, permissions: list[Permission]):
        updated_user_permissions = user.permissions[:] + permissions
        self.update_user_permissions(user, updated_user_permissions)

    @trace()
    def remove_user_permissions(self, user: User, permissions: list[Permission]):
        updated_user_permissions = list(set(user.permissions[:]) - set(permissions))
        self.update_user_permissions(user, updated_user_permissions)

    @trace()
    def update_user_permissions(self, user: User, permissions: list[Permission]):
        user.permissions = list(set(permissions))
        db.session.commit()

    def has_perms(self, user_id, permissions_codenames: list[str], condition=ConditionsEnum.AND) -> bool:
        for i in range(len(permissions_codenames)):
            permissions_codenames[i] = permissions_codenames[i].lower()

        user = self.get_user_by_id(user_id)

        permissions = (
            Permission.query.join(Permission.users)
            .filter(User.id == user.id, Permission.codename.in_(permissions_codenames))
            .all()
        )

        user_has_perms = False
        if condition == ConditionsEnum.AND:
            user_has_perms = len(permissions_codenames) == len(permissions)
        elif condition == ConditionsEnum.OR:
            user_has_perms = len(permissions) > 0

        return user_has_perms
