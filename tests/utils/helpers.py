from tests.functional.settings import test_settings


def add_test_prefix(input_string: str) -> str:
    return f"{test_settings.PREFIX_FOR_FAKE_OBJECTS}-{input_string}"
