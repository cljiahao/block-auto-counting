from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from db.models.color_specs import ColorSpecs

from datetime import datetime as dt
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID

from db.base import Base


class AccuracyProfile(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date_created: Mapped[dt] = mapped_column(default=func.now())
    date_updated: Mapped[dt] = mapped_column(default=func.now(), onupdate=func.now())
    material: Mapped[str] = mapped_column(index=True, nullable=False)
    defect_mode: Mapped[str] = mapped_column(nullable=False)
    count: Mapped[str] = mapped_column(nullable=False)
    area: Mapped[str] = mapped_column(nullable=False)

    # Relationship to ColorSpecs
    color_specs: Mapped[ColorSpecs] = relationship(
        "ColorSpecs", back_populates="accuracy_profile"
    )
    # Foreign key to ColorSpecs
    color_specs_id: Mapped[UUID] = mapped_column(ForeignKey("colorspecs.id"))

    def __repr__(self):
        return f"<AccuracyProfile(id={self.id}, material='{self.material}, defect_mode='{self.defect_mode}')>"
