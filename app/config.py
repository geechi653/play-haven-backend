from os import getenv
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv(".env")

class BaseConfig:
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APISPEC_SWAGGER_UI_URL = "/docs"
    APISPEC_TITLE = "Play Haven API"
    APISPEC_VERSION = "1.0.0"
    SECRET_KEY = getenv("SECRET_KEY")
    JWT_SECRET_KEY = getenv("JWT_SECRET_KEY", getenv("SECRET_KEY"))
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    STEAM_API_KEY = getenv("STEAM_API_KEY")

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite+pysqlite:///:memory:"
    TESTING = True

class ProductionConfig(BaseConfig):
    DEBUG = False

def get_config(env):
    return {
        "development": DevelopmentConfig,
        "testing": TestConfig,
        "production": ProductionConfig,
    }.get(env or getenv("FLASK_ENV", "development"))