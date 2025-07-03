from sqlalchemy.orm import Session

from db.models.block_data import BlockData
from db.repository.base_repository import BaseRepository


class BlockDataRepository(BaseRepository[BlockData]):
    def __init__(self, db: Session):
        super().__init__(db, BlockData)

    def create_block_data(self, block_data: dict) -> list[BlockData]:
        """Create new block data"""
        return self.create(
            block_data,
            print_message="Error creating new data into BlockData database.",
        )

    def read_block_data(self, filter_conditions: dict) -> list[BlockData]:
        """Read block data based on filter"""
        return self.read(
            filter_conditions,
            print_message="Error reading data from BlockData database.",
        )

    def update_block_data(self, update_lists: list[dict[str, dict]]) -> int:
        """Update block data with provided data"""
        return self.update(
            update_lists,
            print_message="Error updating data in BlockData database.",
        )

    def delete_block_data(self, filter_conditions: dict) -> int:
        """Delete block data based on filter"""
        return self.delete(
            filter_conditions,
            print_message="Error deleting data from BlockData database.",
        )
