from http import HTTPStatus

import pytest

from movies_auth.app.models import User
from tests.utils.url import url_builder_v1


class TestSignup:
    @pytest.fixture(autouse=True)
    def setup_method(self, test_client, fake_db, non_existent_user):
        self.test_client = test_client
        self.fake_db = fake_db
        self.non_existent_user = non_existent_user
        self.url = url_builder_v1.build_url("auth.signup")

    @pytest.mark.parametrize("request_body", ({}, {"wrong_key": "some_value"}))
    def test_should_return_bad_request(self, request_body):
        response = self.test_client.post(self.url, json=request_body)

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_try_to_create_existed_user(self):
        user = User.query.first()
        request_body = {"login": user.login, "password": "pwd"}

        response = self.test_client.post(self.url, json=request_body)

        assert response.status_code == HTTPStatus.CONFLICT

    def test_should_return_created(self):
        request_body = {"login": self.non_existent_user.login, "password": "123"}

        response = self.test_client.post(self.url, json=request_body)

        assert response.status_code == HTTPStatus.CREATED

    def test_user_should_be_created_in_db(self):
        request_body = {"login": self.non_existent_user.login, "password": "123"}

        self.test_client.post(self.url, json=request_body)
        created_user = User.query.filter_by(login=self.non_existent_user.login).first()

        assert created_user is not None
        assert created_user.login == self.non_existent_user.login
