from pydantic import Field
from pydantic_settings import BaseSettings


class CommonSettings(BaseSettings):
    """Common settings for the application"""

    PROJECT_NAME: str = Field(default="My Project")
    PROJECT_VERSION: str = Field(default="v1.0.0")
    ENV_STAGE: str = Field(default="dev")
    TROUBLE: str = Field(default="false")


class DatabaseSettings(BaseSettings):
    """Database configuration settings"""

    DB_NAME: str = Field(default="local.db")


class ServiceSettings(BaseSettings):
    """Service-specific settings"""

    TEST_LOT_NO: str = Field(default="1234567890")
    TEST_ITEM: str = Field(default="GJM0225C1ER20WB01_+A01-E0136")
    LIGHT_IPV4: str = Field(default="192.168.0.2")
    LIGHT_PORT: str = Field(default="40001")
    PRASS_URL: str = Field(default="")
    QUANTITY_COLUMN: str = Field(default="")
    ITEM_COLUMN: str = Field(default="")
    FILE_SERVER: str = Field(default="")


# Instantiate settings
common_settings = CommonSettings()
database_settings = DatabaseSettings()
service_settings = ServiceSettings()
