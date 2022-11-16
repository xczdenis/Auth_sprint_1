from app.utils import get_parameter_from_request


def get_provider_from_request(**kwargs):
    return get_parameter_from_request("provider", **kwargs)
