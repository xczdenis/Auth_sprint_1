import pytest

from movies_auth.app.models import User
from tests.custom_faker import faker
from tests.utils.db import delete_object_by_attribute


@pytest.fixture(scope="function")
def non_existent_user() -> User:
    unique_user_login = faker.unique_user_login()
    pwd = "pwd!"

    user = faker.app_user(unique_user_login, pwd)

    yield user

    delete_object_by_attribute(user, "login")


@pytest.fixture(scope="function")
def existing_user_and_his_password() -> tuple[User, str]:
    unique_user_login = faker.unique_user_login()
    password = "Password123!"

    user = faker.app_user(unique_user_login, password)
    user.save()

    yield user, password

    delete_object_by_attribute(user, "login")
