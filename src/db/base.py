from typing import Any, Type
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase

from core.logging import logger
from db.session import engine


class Base(DeclarativeBase):
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls: Type["Base"]) -> str:
        """Generate table name from class name"""
        return cls.__name__.lower()


def create_tables() -> None:
    """Create database tables based on the metadata"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created.")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise
