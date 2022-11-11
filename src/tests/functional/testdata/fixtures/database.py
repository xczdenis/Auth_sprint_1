import pytest

from app import db
from app.models import Permission, User
from tests.functional.testdata.data_generators import (
    generate_permissions,
    generate_users,
)


@pytest.fixture(scope="session")
def fake_db(app):
    users = generate_users(50)
    permissions = generate_permissions()

    def clean_data():
        db.session.query(User).filter(User.id.in_([_.id for _ in users])).delete()
        db.session.query(Permission).filter(Permission.id.in_([_.id for _ in permissions])).delete()
        db.session.commit()

    clean_data()

    db.session.bulk_save_objects(users)
    db.session.bulk_save_objects(permissions)
    db.session.commit()

    yield db

    clean_data()


@pytest.fixture(scope="session")
def unique_unsaved_user(app):
    login = "unique"
    n = 0
    while User.query.filter_by(login=login).first() is not None:
        login = f"unique-{n}"
        n += 1

    password = "Password123!"
    user = User()
    user.login = login
    user.set_password(password)

    yield user, password

    User.query.filter_by(login=login).delete()
    db.session.commit()


@pytest.fixture(scope="session")
def unique_saved_user(app):
    login = "unique"
    n = 0
    while User.query.filter_by(login=login).first() is not None:
        login = f"unique-{n}"
        n += 1

    password = "Password123!"
    user = User()
    user.login = login
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    yield user, password

    User.query.filter_by(login=login).delete()
    db.session.commit()


@pytest.fixture(scope="session")
def unique_unsaved_permission(app):
    codename = "unique"
    n = 0
    while Permission.query.filter_by(codename=codename).first() is not None:
        codename = f"unique-{n}"
        n += 1

    permission = Permission()
    permission.codename = codename
    permission.name = codename

    yield permission

    Permission.query.filter_by(codename=codename).delete()
    db.session.commit()
