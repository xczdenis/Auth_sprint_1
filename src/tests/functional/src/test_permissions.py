from http import HTTPStatus

from flask_jwt_extended import create_access_token

from app.models import Permission


def test_permissions_get(test_client, fake_db, unique_saved_user):
    user, pwd = unique_saved_user
    access_token = create_access_token(identity=user.id, additional_claims={"is_superuser": True})
    response = test_client.get(
        "/permissions/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    data = response.json
    assert response.status_code == HTTPStatus.OK
    assert Permission.query.count() == len(data)


def test_permissions_post(test_client, fake_db, unique_saved_user, unique_unsaved_permission):
    user, pwd = unique_saved_user
    access_token = create_access_token(identity=user.id, additional_claims={"is_superuser": True})
    response = test_client.post(
        "/permissions/",
        json={
            "name": unique_unsaved_permission.name,
            "codename": unique_unsaved_permission.codename,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    new_perms = Permission.query.filter_by(codename=unique_unsaved_permission.codename).all()

    assert response.status_code == HTTPStatus.CREATED
    assert len(new_perms) == 1
    assert new_perms[0].codename == unique_unsaved_permission.codename
    assert new_perms[0].name == unique_unsaved_permission.name
