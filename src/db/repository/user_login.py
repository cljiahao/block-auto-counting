from sqlalchemy.orm import Session

from db.models.user_login import UserLogin
from db.repository.base_repository import BaseRepository


class UserLoginRepository(BaseRepository[UserLogin]):
    def __init__(self, db: Session):
        super().__init__(db, UserLogin)

    def create_user_login(self, user_login: dict) -> list[UserLogin]:
        """Create new user login"""
        return self.create(
            user_login,
            print_message="Error creating new data into UserLogin database.",
        )

    def read_user_login(self, filter_conditions: dict) -> list[UserLogin]:
        """Read user login based on filter"""
        return self.read(
            filter_conditions,
            print_message="Error reading data from UserLogin database.",
        )

    def update_user_login(self, update_lists: list[dict[str, dict]]) -> int:
        """Update user login with provided data"""
        return self.update(
            update_lists,
            print_message="Error updating data in UserLogin database.",
        )

    def delete_user_login(self, filter_conditions: dict) -> int:
        """Delete user login based on filter"""
        return self.delete(
            filter_conditions,
            print_message="Error deleting data from UserLogin database.",
        )
