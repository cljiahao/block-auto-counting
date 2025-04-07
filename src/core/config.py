from pathlib import Path
from dotenv import load_dotenv

from pydantic import Field
from pydantic_settings import BaseSettings

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class CommonSettings(BaseSettings):
    """Common settings for the application."""

    PROJECT_NAME: str = Field(default="My Project")
    PROJECT_VERSION: str = Field(default="v1.0.0")
    ENV_STAGE: str = Field(default="dev")


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""

    DB_NAME: str = Field(default="local.db")


# Instantiate settings
common_settings = CommonSettings()
database_settings = DatabaseSettings()
