from tests.utils.helpers import add_test_prefix


def test_prefix(func):
    def wrapper(*args, **kwargs):
        return add_test_prefix(func(*args, **kwargs))

    return wrapper
