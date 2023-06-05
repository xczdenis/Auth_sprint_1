class BaseAppException(Exception):
    """Common base class for all app exception"""

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            self.description = args[0]
        else:
            self.description = kwargs.get("description", "")


class AppHTTPException(BaseAppException):
    """Class for all http exception"""

    def __init__(self, description, code):
        super().__init__(description)
        self.code = code


class Forbidden(BaseAppException):
    pass


class EntityDoesntExists(BaseAppException):
    pass


class EntityAlreadyExists(BaseAppException):
    pass


class AuthenticationError(BaseAppException):
    pass


class OldPasswordIsIncorrect(BaseAppException):
    pass
