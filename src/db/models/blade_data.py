from datetime import datetime as dt
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class BladeData(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date_created: Mapped[dt] = mapped_column(default=func.now())
    date_updated: Mapped[dt] = mapped_column(default=func.now(), onupdate=func.now())
    lot_no: Mapped[str] = mapped_column(String(10), index=True)
    blade_name: Mapped[str]
    blade_type: Mapped[str]
    blade_batch_no: Mapped[str]
    blade_life: Mapped[str]

    def __repr__(self):
        return f"<BladeData(id={self.id}, lot_no='{self.lot_no}', blade_name='{self.blade_name}')>"
