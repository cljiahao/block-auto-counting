from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from db.models.accuracy_profile import AccuracyProfile

from datetime import datetime as dt
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4, UUID

from db.base import Base


class ColorSpecs(Base):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, index=True)
    date_created: Mapped[dt] = mapped_column(default=func.now())
    date_updated: Mapped[dt] = mapped_column(default=func.now(), onupdate=func.now())
    color: Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    is_tape: Mapped[int] = mapped_column(default=0)
    lower_limit: Mapped[str] = mapped_column(nullable=False)
    upper_limit: Mapped[str] = mapped_column(nullable=False)

    # Relationship to AccuracyProfile
    accuracy_profile: Mapped[list[AccuracyProfile]] = relationship(
        "AccuracyProfile", back_populates="color_specs"
    )

    def __repr__(self):
        return f"<ColorSpecs(id={self.id}, color='{self.color}')>"
