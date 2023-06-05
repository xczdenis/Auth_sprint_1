import os
from datetime import timedelta
from pathlib import Path

from pydantic import BaseModel, BaseSettings, Field, validator

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR.parent
ROOT_DIR = SRC_DIR.parent


class Paginator(BaseModel):
    page_size: int = 20
    page_size_query_path: str = "page[size]"
    page_number_query_path: str = "page[number]"


class BaseSettingsConfigMixin(BaseSettings):
    class Config:
        env_file = os.path.join(ROOT_DIR, ".env")
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


class PostgresSettings(BaseSettingsConfigMixin):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str


class JaegerSettings(BaseSettingsConfigMixin):
    JAEGER_HOST: str
    JAEGER_UDP_PORT: int


class RedisSettings(BaseSettingsConfigMixin):
    REDIS_HOST: str
    REDIS_PORT: int


class BaseOAuthProvider(BaseModel):
    authorize_url: str
    access_token_url: str
    api_base_url: str
    userinfo_url: str


class Oauth2Settings(BaseSettingsConfigMixin):
    YANDEX_OAUTH: BaseOAuthProvider
    YANDEX_CLIENT_ID: str
    YANDEX_CLIENT_SECRET: str
    MAIL_OAUTH: BaseOAuthProvider
    MAIL_CLIENT_ID: str
    MAIL_CLIENT_SECRET: str
    GOOGLE_OAUTH: BaseOAuthProvider
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str


class AppSettings(BaseSettingsConfigMixin):
    ENVIRONMENT: str = "production"
    PROJECT_NAME: str
    SECRET_KEY: str
    DATABASE_URL: str = ""
    SQLALCHEMY_DATABASE_URI: str = ""
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    APP_HOST: str
    APP_PORT: int
    RPS_LIMIT: int
    PAGINATOR: Paginator = Paginator()
    ENABLE_TRACER: bool = True
    DEBUG: bool = False
    RELOAD: bool = False
    JWT_SECRET_KEY: str = Field(env="SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(hours=5)
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = timedelta(days=30)

    @validator("DEBUG")
    def set_debug(cls, v, values):  # noqa
        return v and values["ENVIRONMENT"] == "development"

    @validator("RELOAD")
    def set_reload(cls, v, values):  # noqa
        return v and values["ENVIRONMENT"] == "development"


oauth2_settings: Oauth2Settings = Oauth2Settings()
postgres_settings: PostgresSettings = PostgresSettings()
redis_settings: RedisSettings = RedisSettings()
jaeger_settings: JaegerSettings = JaegerSettings()
app_settings: AppSettings = AppSettings()
app_settings.SQLALCHEMY_DATABASE_URI = "postgresql://{usr}:{pwd}@{host}:{port}/{db}".format(
    usr=postgres_settings.POSTGRES_USER,
    pwd=postgres_settings.POSTGRES_PASSWORD,
    host=postgres_settings.POSTGRES_HOST,
    port=postgres_settings.POSTGRES_PORT,
    db=postgres_settings.POSTGRES_DB,
)
