import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    ENV_STAGE: str = os.getenv("ENV_STAGE", "debug")
    LOCAL_DB_PATH: str = os.getenv("LOCAL_DB_PATH", "./local.db")
    ADMIN_MESID: str = os.getenv("ADMIN_MESID")


settings = Settings()
