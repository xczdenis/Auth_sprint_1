from enum import Enum


class AuthenticationMethods(str, Enum):
    login_password = "login_password"  # noqa: S105 Possible hardcoded password
    jwt = "jwt"
    oauth2 = "oauth2"


class ConditionsEnum(str, Enum):
    AND = "and"
    OR = "or"
