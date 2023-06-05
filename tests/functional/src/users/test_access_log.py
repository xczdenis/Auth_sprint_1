from http import HTTPStatus

from flask_jwt_extended import create_access_token

from tests.utils.url import url_builder_v1


def test_should_return_ok(test_client, fake_db, existing_user_and_his_password):
    user, pwd = existing_user_and_his_password
    access_token = create_access_token(identity=user.id)
    url = url_builder_v1.build_url("users.access_log")
    headers = {"Authorization": f"Bearer {access_token}"}

    response = test_client.get(url, headers=headers)

    assert response.status_code == HTTPStatus.OK
