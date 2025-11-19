from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING
import uuid
from datetime import datetime
from enum import Enum
from ..db import Base

if TYPE_CHECKING:
    from .todo import Todo
    from .organization import Organization


class UserRole(Enum):
    superuser = "superuser"
    organization_owner = "organization_owner"
    admin = "admin"
    team_lead = "team_lead"
    user = "user"


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    username: Mapped[str] = mapped_column(
        String(collation="NOCASE"), unique=True, index=True, nullable=False
    )
    display_name: Mapped[str] = mapped_column(String, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, onupdate=datetime.now)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[str] = mapped_column(SqlEnum(UserRole), default=UserRole.user)

    organization_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.org_id"))
    organization: Mapped["Organization"] = relationship("Organization", back_populates="users")

    todos: Mapped[List["Todo"]] = relationship(
        "Todo", back_populates="owner", cascade="all, delete-orphan"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "display_name" not in kwargs and "username" in kwargs:
            self.display_name = kwargs["username"]
