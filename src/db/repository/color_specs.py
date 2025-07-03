from sqlalchemy.orm import Session

from db.models.color_specs import ColorSpecs
from db.repository.base_repository import BaseRepository


class ColorSpecsRepository(BaseRepository[ColorSpecs]):
    def __init__(self, db: Session):
        super().__init__(db, ColorSpecs)

    def create_color_specs(self, color_specs: dict) -> list[ColorSpecs]:
        """Create new color settings"""
        return self.create(
            color_specs,
            print_message="Error creating new data into ColorSpecs database.",
        )

    def read_color_specs(self, filter_conditions: dict) -> list[ColorSpecs]:
        """Read color settings based on filter"""
        return self.read(
            filter_conditions,
            print_message="Error reading data from ColorSpecs database.",
        )

    def read_all_color_specs(self) -> list[ColorSpecs]:
        """Read all color settings"""
        return self.read(
            {},
            return_all=True,
            print_message="Error reading data from ColorSpecs database.",
        )

    def update_color_specs(self, update_lists: list[dict[str, dict]]) -> int:
        """Update color settings with provided data"""
        return self.update(
            update_lists,
            print_message="Error updating data in ColorSpecs database.",
        )

    def delete_color_specs(self, filter_conditions: dict) -> int:
        """Delete color settings based on filter"""
        return self.delete(
            filter_conditions,
            print_message="Error deleting data from ColorSpecs database.",
        )
