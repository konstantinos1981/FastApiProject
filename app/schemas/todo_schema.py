from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, Field
from .examples import *
from uuid import UUID



# -----------------------
# Todo Schemas
# -----------------------
class TodoBase(BaseModel):
    title: Annotated[str, Field(min_length=3)]
    description: Optional[str] = None


class TodoCreate(TodoBase):
    """Schema for creating a new todo."""
    pass


class TodoUpdate(BaseModel):
    """Schema for updating an existing todo."""
    title: Optional[str] = Field(None, min_length=3)
    description: Optional[str] = None
    is_completed: Optional[bool] = None


class TodoRead(TodoBase):
    """Schema for reading todo data."""
    id: UUID
    owner_id: int
    is_completed: bool
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": todo_read_example
        }
    }
