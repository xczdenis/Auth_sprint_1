from http import HTTPStatus

from flask_jwt_extended import create_access_token

from tests.utils.url import url_builder_v1


def test_change_password(test_client, fake_db, existing_user_and_his_password):
    user, pwd = existing_user_and_his_password
    new_pwd = "new-pwd"
    access_token = create_access_token(identity=user.id)
    url = url_builder_v1.build_url("users.change_password")
    request_body = {"old_password": pwd, "new_password": new_pwd}
    headers = {"Authorization": f"Bearer {access_token}"}

    response = test_client.post(url, json=request_body, headers=headers)
    assert response.status_code == HTTPStatus.OK

    url = url_builder_v1.build_url("auth.signin")
    request_body = {"login": user.login, "password": pwd}
    response = test_client.post(url, json=request_body)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    url = url_builder_v1.build_url("auth.signin")
    request_body = {"login": user.login, "password": new_pwd}
    response = test_client.post(url, json=request_body)
    assert response.status_code == HTTPStatus.CREATED
