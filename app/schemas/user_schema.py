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
    confirm_password: Annotated[str, Field(min_length=8, max_length=16)]

    @field_validator('confirm_password')
    def passwords_match(cls, v, info):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError("Passwords do not match.")
        return v

    @field_validator('password')
    def validate_password_strength(cls, v):
        rules = [
            (r'.{8,16}', 'Password must be between 8 and 16 characters long.'),
            (r'[A-Z]', 'Password must contain at least one uppercase letter.'),
            (r'[a-z]', 'Password must contain at least one lowercase letter.'),
            (r'[0-9]', 'Password must contain at least one digit.'),
            (r'[!@#$%^&*(),.?":{}|<>]', 'Password must contain at least one special character.')
        ]

        errors = [msg for pattern, msg in rules if not re.search(pattern, v)]
        if errors:
            raise ValueError("\n".join(errors))
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

