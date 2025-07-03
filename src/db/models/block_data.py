from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from db.models.defects_data import DefectsData

from datetime import datetime as dt
from sqlalchemy import func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class BlockData(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date_created: Mapped[dt] = mapped_column(default=func.now())
    date_updated: Mapped[dt] = mapped_column(default=func.now(), onupdate=func.now())
    lot_no: Mapped[str] = mapped_column(String(10), index=True, unique=True)
    payroll_no: Mapped[str] = mapped_column(nullable=False)
    mc_no: Mapped[str] = mapped_column(nullable=False)
    input_qty: Mapped[str] = mapped_column(nullable=False)

    # Relationship to DefectsData
    defects_data: Mapped[list[DefectsData]] = relationship(
        "DefectsData", back_populates="block_data"
    )

    def __repr__(self):
        return f"<BlockData(id={self.id}, lot_no='{self.lot_no}')>"
