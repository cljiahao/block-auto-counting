from sqlalchemy.orm import Session

from core.exceptions import NoResultsFound
from db.models.user_login import UserLogin
from db.repository.user_login import UserLoginRepository
from db.services.base_service import BaseService


class UserLoginService(BaseService):
    def __init__(self, db: Session) -> None:
        """Initialize service with repository"""
        self.repo = UserLoginRepository(db)

    def _validate_user_login_keys(self, user_login: dict) -> None:
        """Validate the keys in the user login data"""
        valid_keys = {
            "password",
            "superuser",
        }
        self._validate_input_keys(user_login, valid_keys, "User Login")

    def read_user_login(self, username: str) -> UserLogin:
        """Service layer method to read user login data"""
        self._validate_value_empty("Username", username)

        filter_conditions = {"username": username}

        return self.repo.read_user_login(filter_conditions)[0]

    def read_user_login_not_empty(self, username: str) -> UserLogin:
        """Service layer method to read user login data, ensure not empty"""
        user_login = self.read_user_login(username)

        if user_login is None:
            raise NoResultsFound(
                f"user login data for '{username}' not found in API or database."
            )
        return user_login

    def create_or_update_user_login(
        self, username: str, user_login: dict[str, int]
    ) -> UserLogin:
        """Service layer method to create new or update user login data"""
        self._validate_value_empty("Username", username)
        self._validate_user_login_keys(user_login)

        filter_conditions = {"username": username}

        existing_settings = self.read_user_login(username)
        if existing_settings:
            self.repo.update_user_login(
                {
                    "filter_conditions": filter_conditions,
                    "update_data": user_login,
                }
            )
            return self.read_user_login_not_empty(username)

        user_login.update(filter_conditions)
        return self.repo.create_user_login(user_login)[0]
