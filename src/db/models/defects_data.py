from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from db.models.block_data import BlockData

from datetime import datetime as dt
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class DefectsData(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date_created: Mapped[dt] = mapped_column(default=func.now())
    date_updated: Mapped[dt] = mapped_column(default=func.now(), onupdate=func.now())
    U1: Mapped[str] = mapped_column(default=0)
    U2: Mapped[str] = mapped_column(default=0)
    U3: Mapped[str] = mapped_column(default=0)
    U4: Mapped[str] = mapped_column(default=0)
    U5: Mapped[str] = mapped_column(default=0)
    U6: Mapped[str] = mapped_column(default=0)
    U7: Mapped[str] = mapped_column(default=0)
    U8: Mapped[str] = mapped_column(default=0)
    U9: Mapped[str] = mapped_column(default=0)
    UA: Mapped[str] = mapped_column(default=0)
    UB: Mapped[str] = mapped_column(default=0)
    UC: Mapped[str] = mapped_column(default=0)
    UD: Mapped[str] = mapped_column(default=0)
    UE: Mapped[str] = mapped_column(default=0)
    UF: Mapped[str] = mapped_column(default=0)
    UK: Mapped[str] = mapped_column(default=0)
    UL: Mapped[str] = mapped_column(default=0)
    UR: Mapped[str] = mapped_column(default=0)
    US: Mapped[str] = mapped_column(default=0)
    UT: Mapped[str] = mapped_column(default=0)
    O1: Mapped[str] = mapped_column(default=0)
    I1: Mapped[str] = mapped_column(default=0)
    L1: Mapped[str] = mapped_column(default=0)

    # Relationship to BlockData
    block_data: Mapped[BlockData] = relationship(
        "BlockData", back_populates="defects_data"
    )
    # Foreign key to BlockData
    block_data_lot_no: Mapped[str] = mapped_column(ForeignKey("blockdata.lot_no"))

    def __repr__(self):
        return (
            f"<BlockData(id={self.id}, block_data_lot_no='{self.block_data_lot_no}')>"
        )
