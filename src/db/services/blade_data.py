from sqlalchemy.orm import Session

from core.exceptions import NoResultsFound
from db.models.blade_data import BladeData
from db.repository.blade_data import BladeDataRepository
from db.services.base_service import BaseService


class BladeDataService(BaseService):
    def __init__(self, db: Session) -> None:
        """Initialize service with repository"""
        self.repo = BladeDataRepository(db)

    def _validate_blade_data_keys(self, blade_data: dict) -> None:
        """Validate the keys in the blade data"""
        valid_keys = {
            "blade_name",
            "blade_type",
            "blade_batch_no",
            "blade_life",
        }
        self._validate_input_keys(blade_data, valid_keys, "Blade")

    def read_blade_data(self, lot_no: str) -> BladeData:
        """Service layer method to read blade data"""
        self._validate_value_empty("Lot No", lot_no)

        filter_conditions = {"lot_no": lot_no}

        return self.repo.read_blade_data(filter_conditions)[0]

    def read_blade_data_not_empty(self, lot_no: str) -> BladeData:
        """Service layer method to read blade data, ensure not empty"""
        blade_data = self.read_blade_data(lot_no)

        if blade_data is None:
            raise NoResultsFound(
                f"Blade data for '{lot_no}' not found in API or database."
            )
        return blade_data

    def create_or_update_blade_data(
        self, lot_no: str, blade_data: dict[str, int]
    ) -> BladeData:
        """Service layer method to create new or update blade data"""
        self._validate_value_empty("Lot No", lot_no)
        self._validate_blade_data_keys(blade_data)

        filter_conditions = {"lot_no": lot_no}

        existing_settings = self.read_blade_data(lot_no)
        if existing_settings:
            self.repo.update_blade_data(
                {
                    "filter_conditions": filter_conditions,
                    "update_data": blade_data,
                }
            )
            return self.read_blade_data_not_empty(lot_no)

        blade_data.update(filter_conditions)
        return self.repo.create_blade_data(blade_data)[0]
