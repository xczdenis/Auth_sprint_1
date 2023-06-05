from http import HTTPStatus

from flasgger import swag_from
from flask import jsonify, redirect, request
from flask_jwt_extended import jwt_required

from movies_auth.app import oauth_manager
from movies_auth.app.api.v1.oauth import bp
from movies_auth.app.common.decorators import paginate, superuser_required
from movies_auth.app.common.pagination import get_pagination_params
from movies_auth.app.common.utils import obtain_auth_tokens
from movies_auth.app.models import SocialAccount, User
from movies_auth.app.oauth2.utils import get_provider_from_request


@bp.route("/authorize-url", methods=["POST"])
@swag_from("docs/authorize_url.yml")
def authorize_url():
    return jsonify(oauth_manager.make_authorize_data())


@bp.route("/authorize", methods=["GET", "POST"])
@swag_from("docs/authorize_post.yml", methods=["POST"])
def authorize():
    if request.method == "GET":
        return redirect(oauth_manager.generate_client_redirect_uri())

    provider_name = get_provider_from_request()
    oauth_social_account = oauth_manager.get_social_account(provider_name=provider_name)

    user = User.get_or_create(login=oauth_social_account.login, email=oauth_social_account.email)
    SocialAccount.get_or_create(
        provider=provider_name,
        social_id=oauth_social_account.id,
        email=oauth_social_account.email,
        login=oauth_social_account.login,
        user=user,
    )

    tokens = obtain_auth_tokens(user.id, user.is_superuser)

    return jsonify(**tokens), HTTPStatus.CREATED


@bp.route("/social-accounts", methods=["GET"])
@jwt_required()
@superuser_required()
@paginate()
def users():
    page_number, page_size = get_pagination_params()
    return SocialAccount.query.paginate(page=page_number, per_page=page_size)
