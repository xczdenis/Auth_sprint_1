from flask_jwt_extended import create_access_token


def test_access_log(test_client, unique_saved_user):
    user, pwd = unique_saved_user
    access_token = create_access_token(identity=user.id)
    response = test_client.get(
        "/users/access_log/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200


def test_change_password(test_client, unique_saved_user):
    user, pwd = unique_saved_user
    new_pwd = "new-pwd"
    access_token = create_access_token(identity=user.id)
    response = test_client.post(
        "/users/change_password/",
        json={"old_password": pwd, "new_password": new_pwd},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200

    response = test_client.post("/auth/signin/", json={"login": user.login, "password": pwd})
    assert response.status_code == 401

    response = test_client.post("/auth/signin/", json={"login": user.login, "password": new_pwd})
    assert response.status_code == 201
