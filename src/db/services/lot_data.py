from sqlalchemy.orm import Session

from core.exceptions import NoResultsFound
from db.models.block_data import BlockData
from db.models.defects_data import DefectsData
from db.repository.block_data import BlockDataRepository
from db.repository.defects_data import DefectsDataRepository
from db.services.base_service import BaseService


class LotDataService(BaseService):
    def __init__(self, db: Session) -> None:
        """Initialize service with repository"""
        self.block_data_repo = BlockDataRepository(db)
        self.defects_data_repo = DefectsDataRepository(db)

    def _validate_block_data_keys(self, block_data: dict) -> None:
        """Validate the keys in the block data"""
        valid_keys = {
            "payroll_no",
            "mc_no",
            "input_qty",
        }
        self._validate_input_keys(block_data, valid_keys, "Block")

    def _validate_defects_data_keys(self, defects_data: dict) -> None:
        """Validate the keys in the defects data"""
        valid_keys = {
            "U1",
            "U2",
            "U3",
            "U4",
            "U5",
            "U6",
            "U7",
            "U8",
            "U9",
            "UA",
            "UB",
            "UC",
            "UD",
            "UE",
            "UF",
            "UK",
            "UL",
            "UR",
            "US",
            "UT",
            "O1",
            "I1",
            "L1",
        }
        self._validate_input_keys(defects_data, valid_keys, "Defects")

    def read_block_data(self, lot_no: str) -> BlockData:
        """Service layer method to read block data"""
        self._validate_value_empty("Lot No", lot_no)

        filter_conditions = {"lot_no": lot_no}

        return self.block_data_repo.read_block_data(filter_conditions)[0]

    def read_block_data_not_empty(self, lot_no: str) -> BlockData:
        """Service layer method to read Lot No, ensure not empty"""
        block_data = self.read_block_data(lot_no)

        if block_data is None:
            raise NoResultsFound(
                f"Block Data for '{lot_no}' not found in API or database."
            )
        return block_data

    def create_or_update_block_data(
        self, lot_no: str, block_data: dict[str, int]
    ) -> BlockData:
        """Service layer method to create new or update Lot No"""
        self._validate_value_empty("Lot No", lot_no)
        self._validate_block_data_keys(block_data)

        filter_conditions = {"lot_no": lot_no}

        existing_settings = self.read_block_data(lot_no)
        if existing_settings:
            self.block_data_repo.update_block_data(
                {
                    "filter_conditions": filter_conditions,
                    "update_data": block_data,
                }
            )
            return self.read_block_data_not_empty(lot_no)

        block_data.update(filter_conditions)
        return self.block_data_repo.create_block_data(block_data)[0]

    def create_defects_data(
        self, lot_no: str, defects_data: dict[str, str]
    ) -> DefectsData:
        self._validate_value_empty("Lot No", lot_no)
        self._validate_defects_data_keys(defects_data)

        self.read_block_data_not_empty(lot_no)

        filter_conditions = {"block_data_lot_no": lot_no}
        defects_data.update(filter_conditions)
        return self.defects_data_repo.create_defects_data(defects_data)

    def delete_defects_data(self, defects_id: str) -> int:
        filter_condition = {"id": defects_id}
        return self.defects_data_repo.delete_defects_data(filter_condition)
