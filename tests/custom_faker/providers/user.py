import uuid

from faker import Faker
from faker.providers import BaseProvider

from movies_auth.app.models import User
from tests.utils.decorators import test_prefix

local_faker = Faker()


class UserProvider(BaseProvider):
    @test_prefix
    def app_user_login(self) -> str:
        return local_faker.user_name()

    def app_user_id(self) -> str:
        return str(uuid.uuid4())

    def app_users(self, items_number: int) -> list[User]:
        return [self.app_user() for _ in range(items_number)]

    def app_user(self, login: str = "", pwd: str = "") -> User:
        user = User()
        user.id = self.app_user_id()
        user.login = login or self.app_user_login()
        user.set_password(pwd or local_faker.password())
        return user

    @test_prefix
    def unique_user_login(self) -> str:
        login = "unique"
        n = 0
        while User.query.filter_by(login=login).first() is not None:
            login = f"unique-{n}"
            n += 1
        return login
