from sqlalchemy import String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import uuid
from ..db import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User  


class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    title: Mapped[str | None] = mapped_column(String, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    owner_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, onupdate=datetime.now)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)

    owner: Mapped["User"] = relationship("User", back_populates="todos")

    


