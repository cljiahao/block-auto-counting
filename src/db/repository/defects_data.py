from sqlalchemy.orm import Session

from db.models.defects_data import DefectsData
from db.repository.base_repository import BaseRepository


class DefectsDataRepository(BaseRepository[DefectsData]):
    def __init__(self, db: Session):
        super().__init__(db, DefectsData)

    def create_defects_data(self, defects_data: dict) -> list[DefectsData]:
        """Create new defects data"""
        return self.create(
            defects_data,
            print_message="Error creating new data into DefectsData database.",
        )

    def read_defects_data(self, filter_conditions: dict) -> list[DefectsData]:
        """Read defects data based on filter"""
        return self.read(
            filter_conditions,
            print_message="Error reading data from DefectsData database.",
        )

    def read_all_defects_data_by_condition(
        self, filter_conditions: dict
    ) -> list[DefectsData]:
        """Read all defects data based on filter"""
        return self.read(
            filter_conditions,
            return_all=True,
            print_message="Error reading data from DefectsData database.",
        )

    def update_defects_data(self, update_lists: list[dict[str, dict]]) -> int:
        """Update defects data with provided data"""
        return self.update(
            update_lists,
            print_message="Error updating data in DefectsData database.",
        )

    def delete_defects_data(self, filter_conditions: dict) -> int:
        """Delete defects data based on filter"""
        return self.delete(
            filter_conditions,
            print_message="Error deleting data from DefectsData database.",
        )
