from datetime import datetime as dt
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class UserLogin(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date_created: Mapped[dt] = mapped_column(default=func.now())
    date_updated: Mapped[dt] = mapped_column(default=func.now(), onupdate=func.now())
    username: Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    superuser: Mapped[int] = mapped_column(default=0)

    def __repr__(self):
        return f"<UserLogin(id={self.id}, key_name='{self.key_name}', value='{self.value}')>"
