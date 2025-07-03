import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Generic, TypeVar, Type

from core.exceptions import NoResultsFound
from utils.debug import error_handler

# Define generic types for the model
T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Base repository class to handle CRUD operations.

    Args:
        db: SQLAlchemy session object
        model: SQLAlchemy model class

    Attributes
        db: SQLAlchemy session object
        model: SQLAlchemy model class
    """

    def __init__(self, db: Session, model: Type[T]) -> None:
        self.db = db
        self.model = model

    def _build_filter(self, filters: dict) -> list:
        """Build filter conditions dynamically"""
        if not filters:
            raise ValueError("Filters cannot be empty.")
        conditions = []
        for key, value in filters.items():
            if hasattr(self.model, key):
                conditions.append(getattr(self.model, key) == value)
            else:
                raise AttributeError(
                    f"Model '{self.model.__name__}' has no attribute '{key}'"
                )
        return conditions

    @error_handler()
    def create(
        self,
        data: dict | list[dict],
        print_message: str = "Error creating new data into the database.",
    ) -> list[T]:
        """Create one or multiple record"""
        try:
            if isinstance(data, list):
                # Bulk create case
                instances = [self.model(**item) for item in data]
                self.db.add_all(instances)
                self.db.commit()
                for instance in instances:
                    self.db.refresh(instance)
                return instances
            else:
                # Single create case
                instance = self.model(**data)
                self.db.add(instance)
                self.db.commit()
                self.db.refresh(instance)
                return [instance]
        except Exception as e:
            self.db.rollback()
            raise SQLAlchemyError(print_message) from e

    @error_handler()
    def read(
        self,
        filter_conditions: dict,
        return_all: bool = False,
        print_message: str = "Error reading data from database.",
    ) -> list[T]:
        """Read one or multiple record"""
        try:
            if filter_conditions:
                conditions = self._build_filter(filter_conditions)
                statement = sa.select(self.model).filter(sa.and_(*conditions))
            else:
                statement = sa.select(self.model)
            result = self.db.execute(statement)
            if return_all:
                return result.scalars().all()
            return [result.scalars().first()]
        except Exception as e:
            self.db.rollback()
            raise SQLAlchemyError(print_message) from e

    @error_handler()
    def update(
        self,
        update_conditions: dict[str, dict] | list[dict[str, dict]],
        print_message: str = "Error updating data in database.",
    ) -> int:
        """Update one or multiple record"""
        try:
            if isinstance(update_conditions, dict):
                # Single update case
                missing_key = {
                    "filter_conditions",
                    "update_data",
                } - update_conditions.keys()
                if missing_key:
                    raise KeyError(f"Missing key {missing_key}")
                conditions = self._build_filter(update_conditions["filter_conditions"])
                statement = sa.select(self.model).filter(sa.and_(*conditions))
                result = self.db.execute(statement)
                instance = result.scalar_one_or_none()
                if not instance:
                    raise NoResultsFound("No matching record found to update.")
                for key, value in update_conditions["update_data"].items():
                    setattr(instance, key, value)
                self.db.commit()
                self.db.refresh(instance)
                return 1
            elif isinstance(update_conditions, list):
                # Bulk update case
                count = 0
                for update_item in update_conditions:
                    missing_key = {
                        "filter_conditions",
                        "update_data",
                    } - update_item.keys()
                    if missing_key:
                        raise KeyError(f"Missing key {missing_key}")

                    conditions = self._build_filter(update_item["filter_conditions"])
                    statement = (
                        sa.update(self.model)
                        .where(sa.and_(*conditions))
                        .values(**update_item["update_data"])
                    )
                    result = self.db.execute(statement)
                    count += result.rowcount
                self.db.commit()
                self.db.expire_all()
                return count
            else:
                raise ValueError(
                    "Invalid input: updates must be a dict or list of dicts."
                )
        except NoResultsFound:
            raise
        except Exception as e:
            self.db.rollback()
            raise SQLAlchemyError(print_message) from e

    @error_handler()
    def delete(
        self,
        filter_conditions: dict | list[dict],
        print_message: str = "Error deleting data from database.",
    ) -> int:
        """Delete one or multiple record"""
        try:
            if isinstance(filter_conditions, list):
                # Bulk delete case
                count = 0
                for filters in filter_conditions:
                    conditions = self._build_filter(filters)
                    statement = sa.delete(self.model).filter(sa.and_(*conditions))
                    result = self.db.execute(statement)
                    count += result.rowcount
                self.db.commit()
                self.db.expire_all()
                return count
            else:
                # Single delete case
                conditions = self._build_filter(filter_conditions)
                statement = sa.delete(self.model).filter(sa.and_(*conditions))
                result = self.db.execute(statement)
                if result.rowcount == 0:
                    raise NoResultsFound("No record found to delete.")
                self.db.commit()
                self.db.expire_all()
                return result.rowcount
        except NoResultsFound:
            raise
        except Exception as e:
            self.db.rollback()
            raise SQLAlchemyError(print_message) from e
