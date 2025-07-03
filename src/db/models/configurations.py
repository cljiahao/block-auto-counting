from datetime import datetime as dt
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class Configurations(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date_created: Mapped[dt] = mapped_column(default=func.now())
    date_updated: Mapped[dt] = mapped_column(default=func.now(), onupdate=func.now())
    category: Mapped[str] = mapped_column(index=True, default="Misc")
    key_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    value: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f"<Configurations(id={self.id}, key_name='{self.key_name}', value='{self.value}')>"
