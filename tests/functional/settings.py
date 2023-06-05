import os
from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BASE_DIR.parent


class BaseSettingsConfigMixin(BaseSettings):
    class Config:
        env_file = os.path.join(ROOT_DIR, ".env")
        env_file_encoding = "utf-8"


class TestSettings(BaseSettingsConfigMixin):
    FAKE_USERS_COUNT: int = 50
    PREFIX_FOR_FAKE_OBJECTS: str = "tests"


test_settings: TestSettings = TestSettings()
