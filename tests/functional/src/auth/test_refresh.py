import pytest
from flask_jwt_extended import decode_token

from tests.utils.url import url_builder_v1


class TestRefresh:
    @pytest.fixture(autouse=True)
    def setup_method(self, test_client, fake_db, existing_user_and_his_password):
        self.test_client = test_client
        self.fake_db = fake_db
        self.existing_user_and_his_password = existing_user_and_his_password
        self.url = url_builder_v1.build_url("auth.refresh")

    def test_should_return_access_token(self):
        user, pwd = self.existing_user_and_his_password
        refresh_token = self.login_and_get_refresh_token(user.login, pwd)
        headers = {"Authorization": f"Bearer {refresh_token}"}

        response = self.test_client.post(self.url, headers=headers)
        access_token = response.body.get("access_token")
        access_token_data = decode_token(access_token)

        assert access_token_data.get("type") == "access"
        assert access_token_data.get("sub") == str(user.id)

    def login_and_get_refresh_token(self, login: str, pwd: str):
        url_signin = url_builder_v1.build_url("auth.signin")
        request_body = {"login": login, "password": pwd}

        response = self.test_client.post(url_signin, json=request_body)

        return response.body.get("refresh_token")
