from loguru import logger

from movies_auth.app.common.utils import abort_json, get_parameter_from_request
from movies_auth.app.oauth2.enums import OAuthProviders
from movies_auth.app.settings import oauth2_settings


def get_provider_attr_from_settings(provider_name: str, attr_name: str):
    value = ""
    env_name = f"{provider_name}_oauth".upper()
    try:
        provider_settings = getattr(oauth2_settings, env_name)
        value = getattr(provider_settings, attr_name)
    except AttributeError as e:
        logger.error(e)
    return value


def get_provider_from_request(silent: bool = False, **kwargs):
    provider = get_parameter_from_request("provider", **kwargs)
    if not silent and not OAuthProviders.is_valid(provider):
        abort_json("No such provider '%s'" % provider)
    return provider
