from sqlalchemy.orm import Session

from db.models.configurations import Configurations
from db.repository.base_repository import BaseRepository


class ConfigurationsRepository(BaseRepository[Configurations]):
    def __init__(self, db: Session):
        super().__init__(db, Configurations)

    def bulk_create_configurations(
        self, configurations: list[dict]
    ) -> list[Configurations]:
        """Bulk create new configurations"""
        return self.create(
            configurations,
            print_message="Error creating new data into Configurations database.",
        )

    def read_all_configurations(self, filter_conditions: dict) -> list[Configurations]:
        """Read configurations based on filter"""
        return self.read(
            filter_conditions,
            return_all=True,
            print_message="Error reading data from Configurations database.",
        )

    def bulk_update_configurations(self, update_lists: list[dict[str, dict]]) -> int:
        """Bulk update configurations with provided data"""
        return self.update(
            update_lists,
            print_message="Error updating data in Configurations database.",
        )

    def bulk_delete_configurations(self, filter_conditions: list[dict]) -> int:
        """Bulk delete configurations based on filter"""
        return self.delete(
            filter_conditions,
            print_message="Error deleting data from Configurations database.",
        )
