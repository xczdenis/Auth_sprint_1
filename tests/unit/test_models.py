from movies_auth.app.models import User


def test_new_user():
    user = User(login="patkennedy79@gmail.com")
    user.set_password("FlaskIsAwesome")
    assert user.login == "patkennedy79@gmail.com"
    assert user.password != "FlaskIsAwesome"
