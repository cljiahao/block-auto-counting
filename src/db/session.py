from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import common_settings, database_settings
from core.directory_manager import directory_manager as dm

# Database URL configuration
DB_NAME = (
    f"{database_settings.DB_NAME}.db"
    if common_settings.ENV_STAGE == "prod"
    else f"{database_settings.DB_NAME}_{common_settings.ENV_STAGE}.db"
)
SQLALCHEMY_DATABASE_URL = f"sqlite:///{dm.config_dir}/{DB_NAME}"

# Create SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[sessionmaker, None, None]:
    """Provide a SQLAlchemy session for dependency injection in FastAPI"""
    db = SessionLocal()
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()
