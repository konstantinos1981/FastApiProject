from sqlalchemy import String, Boolean, DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING
import uuid
from datetime import datetime
from enum import Enum
from ..db import Base

if TYPE_CHECKING:
    from .user import User


class OrganizationType(Enum):
    non_profit = "non_profit"
    for_profit = "for_profit"
    government = "government"
    other = "other"


class Organization(Base):
    __tablename__ = "organizations"

    org_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    org_name: Mapped[str] = mapped_column(String, nullable=False)
    org_email: Mapped[str] = mapped_column(String, unique=True, index=True)
    org_display_name: Mapped[str] = mapped_column(String, index=True)
    org_owner_id: Mapped[str] = mapped_column(String(36))
    org_type: Mapped[str] = mapped_column(SqlEnum(OrganizationType), default=OrganizationType.for_profit)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, onupdate=datetime.now)

    users: Mapped[List["User"]] = relationship(
        "User", back_populates="organization", cascade="all, delete-orphan"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "org_display_name" not in kwargs and "org_name" in kwargs:
            self.org_display_name = kwargs["org_name"]
