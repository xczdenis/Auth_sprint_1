import uuid
from http import HTTPStatus

from flask_jwt_extended import create_access_token, decode_token

from app.models import User


class TestSignup:
    def test_empty_data(self, test_client):
        response = test_client.post("/auth/signup/", json={})
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_wrong_data(self, test_client):
        response = test_client.post("/auth/signup/", json={"wrong_key": "some_value"})
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_user_exists(self, test_client, fake_db):
        user = User.query.first()
        response = test_client.post("/auth/signup/", json={"login": user.login, "password": "pwd"})
        assert response.status_code == HTTPStatus.CONFLICT

    def test_user_should_be_created(self, test_client, fake_db, unique_unsaved_user):
        user, pwd = unique_unsaved_user
        response = test_client.post("/auth/signup/", json={"login": user.login, "password": pwd})
        data = response.json
        created_user = User.query.filter_by(login=user.login).first()

        assert response.status_code == HTTPStatus.CREATED
        assert data.get("login") == user.login
        assert created_user is not None
        assert created_user.login == user.login


class TestSignin:
    def test_empty_data(self, test_client):
        response = test_client.post("/auth/signin/", json={})
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_wrong_data(self, test_client):
        response = test_client.post("/auth/signin/", json={"wrong_key": "some_value"})
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_incorrect_password(self, test_client, fake_db, unique_saved_user):
        user, pwd = unique_saved_user
        response = test_client.post(
            "/auth/signin/", json={"login": user.login, "password": f"wrong-{pwd}"}
        )
        data = response.json

        access_token = data.get("access_token")
        refresh_token = data.get("refresh_token")

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert access_token is None
        assert refresh_token is None

    def test_correct_password(self, test_client, fake_db, unique_saved_user):
        user, pwd = unique_saved_user
        response = test_client.post("/auth/signin/", json={"login": user.login, "password": pwd})
        data = response.json

        access_token = data.get("access_token")
        refresh_token = data.get("refresh_token")

        assert response.status_code == HTTPStatus.CREATED
        assert access_token is not None
        assert refresh_token is not None

        access_token_data = decode_token(access_token)
        refresh_token_data = decode_token(refresh_token)

        assert access_token_data.get("type") == "access"
        assert access_token_data.get("sub") == str(user.id)
        assert access_token_data.get("is_superuser") == user.is_superuser
        assert access_token_data.get("refresh_token_jti") == refresh_token_data.get("jti")


class TestRefresh:
    def test_should_return_access_token(self, test_client, fake_db, unique_saved_user):
        user, pwd = unique_saved_user
        response = test_client.post("/auth/signin/", json={"login": user.login, "password": pwd})
        data = response.json
        refresh_token = data.get("refresh_token")

        response = test_client.post(
            "/auth/refresh/",
            headers={"Authorization": f"Bearer {refresh_token}"},
        )

        data = response.json
        access_token = data.get("access_token")

        assert response.status_code == HTTPStatus.CREATED
        assert access_token is not None

        access_token_data = decode_token(access_token)

        assert access_token_data.get("type") == "access"
        assert access_token_data.get("sub") == str(user.id)


class TestLogout:
    def test_method_not_allowed(self, test_client):
        response = test_client.get("/auth/logout/", params={})
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_incorrect_token(self, test_client):
        access_token = create_access_token(identity=uuid.uuid4())
        response = test_client.post(
            "/auth/logout/",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_correct_token(self, test_client, unique_saved_user):
        user, pwd = unique_saved_user

        response = test_client.post("/auth/signin/", json={"login": user.login, "password": pwd})
        data = response.json
        access_token = data.get("access_token")

        assert response.status_code == HTTPStatus.CREATED

        response = test_client.get(
            "/users/access_log/", headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == HTTPStatus.OK

        response = test_client.post(
            "/auth/logout/", headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == HTTPStatus.OK

        response = test_client.get(
            "/users/access_log/",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
