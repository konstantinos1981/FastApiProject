from datetime import datetime
from typing import Optional, List, Annotated
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from .examples import *
from app.core.validators import *
from uuid import UUID
from .todo_schema import TodoRead
from app.models.user import UserRole



# -----------------------
# User Schemas
# -----------------------
class UserBase(BaseModel):
    first_name: Annotated[str, Field(min_length=2)]
    last_name: Annotated[str, Field(min_length=2)]
    email: EmailStr
    username: Annotated[str, Field(min_length=8, pattern=r"^[A-Za-z0-9_]+$")]
    role: UserRole = UserRole.user

    @field_validator('email')
    def normalize_email(cls, v):
        return normalize_email_field(v)


    @field_validator('first_name', 'last_name')
    def capitalize_names(cls, v):
        return capitalize_name_fields(v)
    
    @field_validator('username')
    def validate_username(cls, v):
        return validate_username_field(v)


class UserCreate(UserBase):
    password: Annotated[str, Field(min_length=8, max_length=16)]
    confirm_password: Annotated[str, Field(min_length=8, max_length=16)]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra= {
            "example": user_create_example
        }
    )

    @field_validator('confirm_password')
    def passwords_match(cls, v, info):
        return confirm_field_match(v, info.data, 'password', "Passwords do not match.")

    @field_validator('password')
    def validate_password_strength(cls, v):
        return validate_password_field(v)



class UserUpdate(BaseModel):
    """Schema for updating user details."""
    first_name: Optional[str] = Field(None, min_length=2)
    last_name: Optional[str] = Field(None, min_length=2)
    username: Optional[str] = Field(None, min_length=8, pattern=r"^[A-Za-z0-9_]+$")
    email: Optional[EmailStr] = None

    model_config = ConfigDict(
       from_attributes=True,
        json_schema_extra= {
            "example": user_update_example
        }
    )


    @field_validator('email')
    def normalize_email(cls, v):
        return normalize_email_field(v)

    @field_validator('username')
    def validate_username(cls, v):
        return validate_username_field(v)

    @field_validator('first_name', 'last_name', mode='before')
    def capitalize_names(cls, v):
        if v:
            return capitalize_name_fields(v)
        return v
    
    


class UserRead(UserBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict({
        "from_attributes": True,  # allows ORM mode
        "json_schema_extra": {
            "example": user_read_example
        }
    }
    )


class UserPasswordUpdate(BaseModel):
    """Schema for updating user password."""
    old_password: Annotated[str, Field(min_length=8, max_length=16)]
    new_password: Annotated[str, Field(min_length=8, max_length=16)]
    confirm_password: Annotated[str, Field(min_length=8, max_length=16)]
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra= {
            "example": user_password_change_example
        }
    )

    @field_validator('confirm_password')
    def passwords_match(cls, v, info):
        return confirm_field_match(v, info.data, 'new_password', "Passwords do not match.")

    @field_validator('new_password')
    def validate_password_strength(cls, v):
        return validate_password_field(v)
    
    

# -----------------------
# Nested relationship schemas
# -----------------------
class UserWithTodos(UserRead):
    """Schema for reading a user with their todos."""
    todos: List[TodoRead] = []
    
    model_config = ConfigDict({
        "from_attributes": True,
        "json_schema_extra": {
            "example": user_with_todos_example
        }
    }
    )

