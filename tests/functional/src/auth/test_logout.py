import uuid
from http import HTTPStatus

import pytest
from flask_jwt_extended import create_access_token

from tests.utils.url import url_builder_v1


class TestLogout:
    @pytest.fixture(autouse=True)
    def setup_method(self, test_client, fake_db, existing_user_and_his_password):
        self.test_client = test_client
        self.fake_db = fake_db
        self.existing_user_and_his_password = existing_user_and_his_password
        self.url = url_builder_v1.build_url("auth.logout")

    def test_should_return_method_not_allowed(self):
        request_body = {}

        response = self.test_client.get(self.url, json=request_body)

        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_logout_with_incorrect_token(self):
        access_token = create_access_token(identity=uuid.uuid4())
        headers = {"Authorization": f"Bearer {access_token}"}

        response = self.test_client.post(self.url, headers=headers)

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_login_with_correct_credentials_returns_access_token(self):
        user, pwd = self.existing_user_and_his_password
        url = url_builder_v1.build_url("auth.signin")
        request_body = {"login": user.login, "password": pwd}

        response = self.test_client.post(url, json=request_body)

        assert response.status_code == HTTPStatus.CREATED
        assert response.body.get("access_token") is not None

    def test_access_token_is_valid_after_login(self):
        access_token = self.login_and_get_access_token()
        url = url_builder_v1.build_url("users.access_log")
        headers = {"Authorization": f"Bearer {access_token}"}

        response = self.test_client.get(url, headers=headers)

        assert response.status_code == HTTPStatus.OK

    def test_logout_with_correct_token_returns_ok(self):
        access_token = self.login_and_get_access_token()
        url = url_builder_v1.build_url("auth.logout")
        headers = {"Authorization": f"Bearer {access_token}"}

        response = self.test_client.post(url, headers=headers)

        assert response.status_code == HTTPStatus.OK

    def test_access_token_is_invalid_after_logout(self):
        access_token = self.login_and_get_access_token()
        self.logout(access_token)
        url = url_builder_v1.build_url("users.access_log")
        headers = {"Authorization": f"Bearer {access_token}"}

        response = self.test_client.get(url, headers=headers)

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def login_and_get_access_token(self):
        user, pwd = self.existing_user_and_his_password
        url_signin = url_builder_v1.build_url("auth.signin")
        request_body = {"login": user.login, "password": pwd}

        response = self.test_client.post(url_signin, json=request_body)

        return response.body.get("access_token")

    def logout(self, access_token: str):
        url = url_builder_v1.build_url("auth.logout")
        headers = {"Authorization": f"Bearer {access_token}"}
        self.test_client.post(url, headers=headers)
