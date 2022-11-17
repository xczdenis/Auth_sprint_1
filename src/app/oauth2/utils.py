from loguru import logger

from app.utils import get_parameter_from_request
from config import settings


def get_provider_attr_from_settings(provider_env_prefix: str, attr_name: str):
    value = ""
    env_name = f"{provider_env_prefix}_oauth".upper()
    try:
        provider_settings = getattr(settings, env_name)
        value = getattr(provider_settings, attr_name)
    except AttributeError as e:
        logger.error(e)
    return value


def get_provider_from_request(**kwargs):
    return get_parameter_from_request("provider", **kwargs)
