from http import HTTPStatus

import pytest
from flask_jwt_extended import decode_token

from tests.utils.url import url_builder_v1


class TestSignin:
    @pytest.fixture(autouse=True)
    def setup_method(self, test_client, fake_db, existing_user_and_his_password):
        self.test_client = test_client
        self.fake_db = fake_db
        self.existing_user_and_his_password = existing_user_and_his_password
        self.url = url_builder_v1.build_url("auth.signin")

    @pytest.mark.parametrize("request_body", ({}, {"wrong_key": "some_value"}))
    def test_should_return_bad_request(self, request_body):
        response = self.test_client.post(self.url, json=request_body)

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_incorrect_password(self):
        user, pwd = self.existing_user_and_his_password
        request_body = {"login": user.login, "password": f"wrong-{pwd}"}

        response = self.test_client.post(self.url, json=request_body)

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.body.get("access_token") is None
        assert response.body.get("refresh_token") is None

    def test_correct_password(self):
        user, pwd = self.existing_user_and_his_password
        request_body = {"login": user.login, "password": pwd}

        response = self.test_client.post(self.url, json=request_body)
        data = response.body

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
