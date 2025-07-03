import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from core.exceptions import NoResultsFound
from db.models.accuracy_profile import AccuracyProfile
from db.models.color_specs import ColorSpecs
from db.repository.accuracy_profile import AccuracyProfileRepository
from db.repository.color_specs import ColorSpecsRepository
from db.services.base_service import BaseService


class ColorSettingsService(BaseService):
    def __init__(self, db: Session) -> None:
        """Initialize service with repository"""
        self.db = db
        self.color_specs_repo = ColorSpecsRepository(db)
        self.accuracy_repo = AccuracyProfileRepository(db)

    def _validate_color_specs_keys(self, color_specs: dict) -> None:
        """Validate the keys in the color specs"""
        valid_keys = {
            "is_tape",
            "lower_limit",
            "upper_limit",
        }
        self._validate_input_keys(color_specs, valid_keys, "ColorSpecs")

    def _validate_accuracy_profile_keys(self, accuracy_profile: dict) -> None:
        """Validate the keys in the accuracy profile"""
        valid_keys = {
            "material",
            "defect_mode",
            "count",
            "area",
        }
        self._validate_input_keys(accuracy_profile, valid_keys, "Accuracy Profile")

    def read_all_color_specs(self) -> list[ColorSpecs]:
        """Service layer method to read all color specs"""
        return self.color_specs_repo.read_all_color_specs()

    def read_color_specs(self, color: str) -> ColorSpecs:
        """Service layer method to read color specs"""
        self._validate_value_empty("Color name", color)

        filter_conditions = {"color": color}

        return self.color_specs_repo.read_color_specs(filter_conditions)[0]

    def read_color_specs_not_empty(self, color: str) -> ColorSpecs:
        """Service layer method to read color specs, ensure not empty"""
        color_specs = self.read_color_specs(color)

        if color_specs is None:
            raise NoResultsFound(
                f"Color specs for '{color}' not found in API or database."
            )
        return color_specs

    def read_all_accuracy_profile(self) -> list[AccuracyProfile]:
        """Service layer method to read all accuracy profile"""
        return self.accuracy_repo.read_all_accuracy_profile()

    def read_accuracy_profile_not_empty(
        self, color: str, material: str = ""
    ) -> list[AccuracyProfile]:
        """Service layer method to read accuracy profile, ensure not empty"""
        color_specs = self.read_color_specs(color)
        if color_specs is None:
            raise NoResultsFound(
                f"Color specs for '{color}' not found in API or database."
            )

        filter_conditions = {"color_specs_id": color_specs.id}
        if material:
            filter_conditions["material"] = material
        return self.accuracy_repo.read_all_accuracy_profile_by_condition(
            filter_conditions
        )

    def create_or_update_color_specs(
        self, color: str, color_specs: dict[str, int]
    ) -> ColorSpecs:
        """Service layer method to create new or update color specs"""
        self._validate_value_empty("Color name", color)
        self._validate_color_specs_keys(color_specs)

        filter_conditions = {"color": color}
        existing_specs = self.read_color_specs(color)
        if existing_specs:
            self.color_specs_repo.update_color_specs(
                {
                    "filter_conditions": filter_conditions,
                    "update_data": color_specs,
                }
            )
            return self.read_color_specs_not_empty(color)

        color_specs.update(filter_conditions)
        return self.color_specs_repo.create_color_specs(color_specs)[0]

    def create_or_update_accuracy_profile(
        self, color: str, material: str, accuracy_profile: dict[str, str]
    ) -> AccuracyProfile:
        """Service layer method to create new or update accuracy profile tagging to specific color"""
        self._validate_value_empty("Color name", color)
        self._validate_value_empty("Material type", material)
        self._validate_accuracy_profile_keys(accuracy_profile)

        color_specs = self.read_color_specs_not_empty(color)

        filter_conditions = {"color_specs_id": color_specs.id, "material": material}
        existing_profile = self.accuracy_repo.read_all_accuracy_profile_by_condition(
            filter_conditions
        )
        if existing_profile:
            self.accuracy_repo.update_accuracy_profile(
                {
                    "filter_conditions": filter_conditions,
                    "update_data": accuracy_profile,
                }
            )
            return self.read_accuracy_profile_not_empty(color, material)

        accuracy_profile.update(filter_conditions)
        return self.accuracy_repo.create_accuracy_profile(accuracy_profile)

    def delete_color_specs(self, color: str) -> int:
        """Service layer method to delete specific color specs and its accuracy profiles"""
        self._validate_value_empty("Color name", color)

        color_specs = self.read_color_specs_not_empty(color)
        accuracy_profile = color_specs.accuracy_profile
        color_specs_condition = {"color": color}
        acc_profile_condition = {"color_specs_id": color_specs.id}

        if accuracy_profile:
            self.accuracy_repo.delete_accuracy_profile(acc_profile_condition)
        return self.color_specs_repo.delete_color_specs(color_specs_condition)

    def delete_accuracy_profile(self, color: str, material: str) -> int:
        """Service layer method to delete accuracy profiles based on color and material"""
        self._validate_value_empty("Color name", color)
        self._validate_value_empty("Material type", material)

        color_specs = self.read_color_specs_not_empty(color)
        acc_profile_condition = {"color_specs_id": color_specs.id, "material": material}

        return self.accuracy_repo.delete_accuracy_profile(acc_profile_condition)

    def get_color_names_by_material(self, material: str) -> list[dict[str, str]]:
        """Service layer method to retrieve colors and accuracy profile based on material"""
        try:
            self._validate_value_empty("Material type", material)

            statement = (
                sa.select(
                    ColorSpecs.color,
                    AccuracyProfile.defect_mode,
                    AccuracyProfile.count,
                    AccuracyProfile.area,
                )
                .join(ColorSpecs.accuracy_profile)
                .filter(AccuracyProfile.material == material)
                .distinct()
            )
            result = self.db.execute(statement)
            return result.mappings().all()
        except Exception as e:
            self.db.rollback()
            raise SQLAlchemyError(
                f"Error fetching color names for material '{material}'."
            ) from e
