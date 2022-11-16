import json
import time
from dataclasses import asdict, dataclass, field
from http import HTTPStatus

from authlib.integrations.flask_client import FlaskOAuth2App, OAuth
from flask import request, session, url_for

from app.decorators import trace
from app.oauth2.utils import get_provider_from_request
from app.utils import (
    abort_json,
    build_url,
    get_parameter_from_request,
    make_key_from_args,
)


@dataclass
class SocialAccount:
    id: str = ""
    name: str = ""
    login: str = ""
    email: str = ""


@dataclass
class BaseOAuthProvider:
    name: str
    userinfo_endpoint: str
    client_kwargs: dict = field(default_factory=lambda: {})
    _client: FlaskOAuth2App | None = None

    def get_metadata(self) -> dict:
        return asdict(self)

    def get_user_info(self) -> dict:
        r = self._client.get(self.userinfo_endpoint)
        return r.json()

    def get_social_account(self) -> SocialAccount | None:
        raise NotImplementedError("Method not implemented!")


@dataclass
class YandexOAuthProvider(BaseOAuthProvider):
    name: str = "yandex"
    userinfo_endpoint: str = "info"
    authorize_url: str = "https://oauth.yandex.ru/authorize"
    access_token_url: str = "https://oauth.yandex.ru/token"
    api_base_url: str = "https://login.yandex.ru"

    def get_social_account(self) -> SocialAccount | None:
        user_info = self.get_user_info()
        if user_info:
            return SocialAccount(
                id=user_info["id"],
                email=user_info["default_email"],
                login=user_info["login"],
                name=user_info["display_name"],
            )
        return None


@dataclass
class MailOAuthProvider(BaseOAuthProvider):
    name: str = "mail"
    userinfo_endpoint: str = "userinfo"
    authorize_url: str = "https://oauth.mail.ru/login"
    access_token_url: str = "https://oauth.mail.ru/token"
    api_base_url: str = "https://oauth.mail.ru"
    client_kwargs: dict = field(default_factory=lambda: {"token_placement": "uri"})

    def get_social_account(self) -> SocialAccount | None:
        user_info = self.get_user_info()
        if user_info:
            return SocialAccount(
                id=user_info["id"],
                email=user_info["email"],
                login=user_info["nickname"],
                name=user_info["first_name"],
            )
        return None


@dataclass
class GoogleOAuthProvider(BaseOAuthProvider):
    name: str = "google"
    userinfo_endpoint: str = "userinfo?alt=json"
    authorize_url: str = "https://accounts.google.com/o/oauth2/v2/auth"
    access_token_url: str = "https://oauth2.googleapis.com/token"
    api_base_url: str = "https://www.googleapis.com/oauth2/v1/"
    client_kwargs: dict = field(
        default_factory=lambda: {
            "scope": "https://www.googleapis.com/auth/userinfo.email "
            "https://www.googleapis.com/auth/userinfo.profile"
        }
    )

    def get_social_account(self) -> SocialAccount | None:
        user_info = self.get_user_info()
        if user_info:
            return SocialAccount(
                id=user_info["id"],
                email=user_info["email"],
                login=user_info["email"],
                name=user_info["given_name"],
            )
        return None


class OAuthManager(OAuth):
    expires_in = 3600
    _authorize_data_key_prefix = "#__authorize_data_key__#"

    def __init__(self, **kwargs):
        self._providers = {}
        super().__init__(**kwargs)

    @property
    def redirect_uri(self):
        url = url_for("api.v1.oauth.authorize", _external=True)
        if not url.endswith("/"):
            url += "/"
        return url

    def register_provider(self, provider: BaseOAuthProvider):
        provider._client = self.register(**provider.get_metadata())
        self._providers[provider.name] = provider

    def get_provider(self, provider_name: str) -> BaseOAuthProvider:
        return self._providers.get(provider_name)

    def get_client(self, provider_name: str, silent: bool = False) -> FlaskOAuth2App:
        try:
            oauth_client = getattr(self, provider_name)
        except AttributeError:
            oauth_client = None
            if not silent:
                abort_json("No client for provider '%s'" % provider_name)
        return oauth_client

    def make_authorize_data(self) -> dict:
        client_redirect_uri = get_parameter_from_request("client_redirect_uri")
        provider_name = get_provider_from_request()
        oauth_client = self.get_client(provider_name)

        authorization_url_data = oauth_client.create_authorization_url(
            redirect_uri=self.redirect_uri
        )
        oauth_client.save_authorize_data(**authorization_url_data)

        self.set_data(
            make_key_from_args(self._authorize_data_key_prefix, authorization_url_data["state"]),
            {
                "state": authorization_url_data["state"],
                "provider": provider_name,
                "client_redirect_uri": client_redirect_uri,
            },
        )

        return authorization_url_data

    def generate_client_redirect_uri(self):
        key = make_key_from_args(self._authorize_data_key_prefix, request.args.get("state"))
        saved_authorize_data = self.get_data(key)
        if not saved_authorize_data:
            abort_json(
                "mismatching_state: CSRF Warning! State not equal in request and response.",
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )
        saved_authorize_data.update(code=request.args.get("code"))
        client_redirect_uri = saved_authorize_data.get("client_redirect_uri")
        return build_url(client_redirect_uri, saved_authorize_data)

    def set_data(self, key, data):
        if self.cache:
            self.cache.set(key, json.dumps({"data": data}), self.expires_in)
        else:
            now = time.time()
            session[key] = {"data": data, "exp": now + self.expires_in}

    def get_data(self, key):
        if self.cache:
            value = self._get_cache_data(key)
        else:
            value = session.get(key)
        if value:
            return value.get("data")
        return None

    def _get_cache_data(self, key):
        value = self.cache.get(key)
        if not value:
            return None
        try:
            return json.loads(value)
        except (TypeError, ValueError):
            return None

    @trace()
    def authorize_access_token(self, provider_name: str, silent: bool = False):
        oauth_client = self.get_client(provider_name)
        try:
            oauth_client.authorize_access_token(redirect_uri=self.redirect_uri)
        except Exception as e:
            if not silent:
                abort_json(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)

    @trace()
    def get_social_account(self, provider_name: str | None = None) -> SocialAccount | None:
        get_parameter_from_request("state")
        get_parameter_from_request("code")
        provider_name = provider_name or get_provider_from_request()
        self.authorize_access_token(provider_name)
        oauth_provider = self.get_provider(provider_name)
        return oauth_provider.get_social_account()
