import pytest

from movies_auth.app import db
from tests.custom_faker import faker
from tests.functional.settings import test_settings
from tests.utils.db import delete_objects_by_id


@pytest.fixture(scope="session")
def fake_db():
    users = faker.app_users(test_settings.FAKE_USERS_COUNT)
    permissions = faker.permissions()

    def clean_data():
        delete_objects_by_id(users)
        delete_objects_by_id(permissions)

    clean_data()

    db.session.bulk_save_objects(users)
    db.session.bulk_save_objects(permissions)
    db.session.commit()

    yield db

    clean_data()
