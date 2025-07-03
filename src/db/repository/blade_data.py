from sqlalchemy.orm import Session

from db.models.blade_data import BladeData
from db.repository.base_repository import BaseRepository


class BladeDataRepository(BaseRepository[BladeData]):
    def __init__(self, db: Session):
        super().__init__(db, BladeData)

    def create_blade_data(self, blade_data: dict) -> list[BladeData]:
        """Create new blade data"""
        return self.create(
            blade_data,
            print_message="Error creating new data into BladeData database.",
        )

    def read_blade_data(self, filter_conditions: dict) -> list[BladeData]:
        """Read blade data based on filter"""
        return self.read(
            filter_conditions,
            print_message="Error reading data from BladeData database.",
        )

    def update_blade_data(self, update_lists: list[dict[str, dict]]) -> int:
        """Update blade data with provided data"""
        return self.update(
            update_lists,
            print_message="Error updating data in BladeData database.",
        )

    def delete_blade_data(self, filter_conditions: dict) -> int:
        """Delete blade data based on filter"""
        return self.delete(
            filter_conditions,
            print_message="Error deleting data from BladeData database.",
        )
