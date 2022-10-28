from faker import Faker

from app.hashers import make_password
from app.models import Permission, User

fake = Faker()


def fake_id():
    return fake.hexify(text="^^^^^^^^-^^^^-^^^^-^^^^-^^^^^^^^^^^^")


def generate_users(items_number: int):
    data = []
    pwd = make_password("raw_password")
    for _ in range(items_number):
        user = User()
        user.id = fake_id()
        user.login = fake.simple_profile()["username"]
        user.password = pwd
        data.append(user)
    return data


def generate_permissions():
    permissions = ["all", "sport", "series", "adult", "new_movies"]
    data = []
    for p in permissions:
        permission = Permission()
        permission.id = fake_id()
        permission.name = p
        permission.codename = p.upper()
        data.append(permission)
    return data
