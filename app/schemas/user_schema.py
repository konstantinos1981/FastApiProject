from datetime import datetime
from typing import Optional, List, Annotated
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
import re
from .examples import *
from uuid import UUID
from .todo_schema import TodoRead


# -----------------------
# User Schemas
# -----------------------
class UserBase(BaseModel):
    first_name: Annotated[str, Field(min_length=2)]
    last_name: Annotated[str, Field(min_length=2)]
    email: EmailStr
    username: Annotated[str, Field(min_length=8, pattern=r"^[A-Za-z0-9_]+$")]

    @field_validator('email')
    def normalize_email(cls, v):
        return v.strip().lower()


    @field_validator('first_name', 'last_name')
    def capitalize_names(cls, v):
        return v.strip().title()


class UserCreate(UserBase):
    password: Annotated[str, Field(min_length=8, max_length=16)]

    @field_validator('password')
    def validate_password_strength(cls, v):
        # Fix: "[A-A]" should be "[A-Z]"
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one number.")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"[\W_]", v):  # special character or underscore
            raise ValueError("Password must contain at least one symbol.")
        return v
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra= {
            "example": user_create_example
        }
)


class UserUpdate(BaseModel):
    """Schema for updating user details."""
    first_name: Optional[str] = Field(None, min_length=2)
    last_name: Optional[str] = Field(None, min_length=2)
    username: Optional[str] = Field(None, min_length=8, pattern=r"^[A-Za-z0-9_]+$")
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

    @field_validator('first_name', 'last_name', mode='before')
    def capitalize_names(cls, v):
        if v:
            return v.strip().title()
        return v


class UserRead(BaseModel):
    id: UUID
    first_name: str
    last_name: Optional[str]
    email: EmailStr
    username: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {
        "from_attributes": True,  # allows ORM mode
        "json_schema_extra": {
            "example": user_read_example
        }
    }


# -----------------------
# Nested relationship schemas
# -----------------------
class UserWithTodos(UserRead):
    """Schema for reading a user with their todos."""
    todos: List[TodoRead] = []
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": user_with_todos_example
        }
    }

