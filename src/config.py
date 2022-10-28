import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = Path(__file__).resolve().parent.parent

env = os.getenv("ENVIRONMENT", "development")

load_dotenv(dotenv_path=os.path.join(ROOT_DIR, ".env"))
load_dotenv(dotenv_path=os.path.join(ROOT_DIR, ".envs", env, ".env"))


def get_db_url():
    db_url = os.getenv("DATABASE_URL", "")
    if not db_url:
        db_url = "postgresql://{usr}:{pwd}@{host}:{port}/{db}".format(
            usr=os.getenv("POSTGRES_USER"),
            pwd=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            db=os.getenv("POSTGRES_DB"),
        )
    return db_url


class Config:
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY", "")

    SQLALCHEMY_DATABASE_URI = get_db_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("SECRET_KEY", "")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
