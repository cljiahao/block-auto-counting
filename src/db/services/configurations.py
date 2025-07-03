from sqlalchemy.orm import Session

from core.exceptions import NoResultsFound
from db.models.configurations import Configurations
from db.repository.configurations import ConfigurationsRepository
from db.services.base_service import BaseService


class ConfigurationsService(BaseService):
    def __init__(self, db: Session) -> None:
        """Initialize service with repository"""
        self.repo = ConfigurationsRepository(db)

    def _validate_configurations_keys(self, configurations: dict) -> None:
        """Validate the keys in the configurations data"""
        valid_keys = {
            "key_name",
            "value",
        }
        self._validate_input_keys(configurations, valid_keys, "Configurations")

    def read_all_configurations_by_category(self, category: str) -> dict[str, str]:
        """Service layer method to read configurations data"""
        self._validate_value_empty("Category", category)

        filter_conditions = {"category": category}

        config_data = self.repo.read_all_configurations(filter_conditions)

        return {
            key: config.value
            for config in config_data
            if (key := getattr(config, "key_name", None)) is not None
        }

    def read_all_configurations_not_empty(self, category: str) -> list[Configurations]:
        """Service layer method to read configurations data, ensure not empty"""
        configurations = self.read_all_configurations_by_category(category)

        if configurations is None:
            raise NoResultsFound(
                f"configurations data for '{category}' not found in API or database."
            )
        return configurations

    def bulk_create_or_update_configurations(
        self, category: str, configurations: list[dict[str, int]]
    ) -> list[Configurations]:
        """Service layer method to create new or update configurations data"""
        self._validate_value_empty("Category", category)

        filter_conditions = {"category": category}

        config_list = []
        for config in configurations:
            self._validate_configurations_keys(config)
            config_list.append(
                {
                    "filter_conditions": {
                        "key_name": config["key_name"],
                        **filter_conditions,
                    },
                    "update_data": {"value": config["value"]},
                }
            )

        existing_settings = self.read_all_configurations_not_empty(category)
        if existing_settings:
            self.repo.bulk_update_configurations(config_list)
            return self.read_all_configurations_not_empty(category)

        return self.repo.bulk_create_configurations(
            [{**configs, **filter_conditions} for configs in configurations]
        )
