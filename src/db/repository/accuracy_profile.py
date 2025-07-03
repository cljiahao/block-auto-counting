from sqlalchemy.orm import Session

from db.models.accuracy_profile import AccuracyProfile
from db.repository.base_repository import BaseRepository


class AccuracyProfileRepository(BaseRepository[AccuracyProfile]):
    def __init__(self, db: Session):
        super().__init__(db, AccuracyProfile)

    def create_accuracy_profile(self, accuracy_profile: dict) -> list[AccuracyProfile]:
        """Create new accuracy profile"""
        return self.create(
            accuracy_profile,
            print_message="Error creating new data into AccuracyProfile database.",
        )

    def read_all_accuracy_profile(self) -> list[AccuracyProfile]:
        """Read accuracy profile based on filter"""
        return self.read(
            {},
            return_all=True,
            print_message="Error reading data from AccuracyProfile database.",
        )

    def read_all_accuracy_profile_by_condition(
        self, filter_conditions: dict
    ) -> list[AccuracyProfile]:
        """Read all accuracy profile based on filter"""
        return self.read(
            filter_conditions,
            return_all=True,
            print_message="Error reading data from AccuracyProfile database.",
        )

    def update_accuracy_profile(self, update_lists: list[dict[str, dict]]) -> int:
        """Update accuracy profile with provided data"""
        return self.update(
            update_lists,
            print_message="Error updating data in AccuracyProfile database.",
        )

    def delete_accuracy_profile(self, filter_conditions: dict) -> int:
        """Delete accuracy profile based on filter"""
        return self.delete(
            filter_conditions,
            print_message="Error deleting data from AccuracyProfile database.",
        )
