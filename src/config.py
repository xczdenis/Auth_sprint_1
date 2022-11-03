import os
from datetime import timedelta
from pathlib import Path

from pydantic import BaseModel, BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = Path(__file__).resolve().parent.parent


def get_db_url(config):
    db_url = config.DATABASE_URL
    if not db_url:
        db_url = "postgresql://{usr}:{pwd}@{host}:{port}/{db}".format(
            usr=config.POSTGRES_USER,
            pwd=config.POSTGRES_PASSWORD,
            host=config.POSTGRES_HOST,
            port=config.POSTGRES_PORT,
            db=config.POSTGRES_DB,
        )
    return db_url


class Paginator(BaseModel):
    page_size: int = 20
    page_size_query_path: str = "page[size]"
    page_number_query_path: str = "page[number]"


class Settings(BaseSettings):
    PROJECT_NAME: str = "movies_auth"
    SECRET_KEY: str
    JWT_SECRET_KEY: str = Field(env="SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = timedelta(days=30)
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    DATABASE_URL: str = ""
    SQLALCHEMY_DATABASE_URI: str = ""
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    APP_HOST: str
    APP_PORT: int
    REDIS_HOST: str
    REDIS_PORT: int
    JAEGER_HOST: str
    JAEGER_UDP_PORT: int
    PAGINATOR: Paginator = Paginator()

    class Config:
        env = os.getenv("ENVIRONMENT", "development")
        env_file = os.path.join(ROOT_DIR, ".envs", env, ".env"), os.path.join(ROOT_DIR, ".env")
        env_file_encoding = "utf-8"


settings = Settings()
settings.SQLALCHEMY_DATABASE_URI = get_db_url(settings)
