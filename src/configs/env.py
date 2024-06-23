"""file to contains env variables"""
import os
from functools import lru_cache
from typing import ClassVar
from pydantic_settings import BaseSettings


class DBConfig:
    """DB configuration class"""
    DB_HOST: str
    DB_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: str


class AppDBConfig:
    """db configuration"""
    db_host = os.getenv('DB_HOST', 'localhost')
    db_name = os.getenv('DB_NAME', 'recipe_db')
    db_username = os.getenv('DB_USERNAME', 'paragmodi26')
    db_password = os.getenv('DB_PASSWORD', '')


class BaseConfig(BaseSettings):
    """base configs"""
    env: str = os.getenv('APP_ENV', 'local')
    db_app: ClassVar[DBConfig] = AppDBConfig
    jwt_secret_key: str = os.getenv('JWT_SECRET_KEY', "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")


@lru_cache()
def get_settings():
    """get env variable"""
    return BaseConfig()

