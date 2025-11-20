from datetime import datetime
from typing import Optional, List, Annotated
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from .examples import *
from app.core.validators import *
from uuid import UUID
from app.models.organization import OrganizationType

# -----------------------
# Organization Schemas
# -----------------------
class OrganizationBase(BaseModel):
    org_name: Annotated[str, Field(min_length=3)]
    org_email: EmailStr
    org_display_name: Optional[Annotated[str, Field(min_length=3)]] = None
    org_type: OrganizationType = OrganizationType.for_profit
    is_active: bool = True

    @field_validator('org_email')
    def normalize_email(cls, v):
        return normalize_email_field(v) 

class OrganizationCreate(OrganizationBase):
    """Schema for creating a new organization."""
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": organization_create_example
        }
    )

class OrganizationUpdate(BaseModel):
    """Schema for updating an existing organization."""
    org_name: Optional[Annotated[str, Field(min_length=3)]] = None
    org_email: Optional[EmailStr] = None
    org_display_name: Optional[Annotated[str, Field(min_length=3)]] = None
    org_type: Optional[OrganizationType] = None
    is_active: Optional[bool] = None

    @field_validator('org_email')
    def normalize_email(cls, v):
        return normalize_email_field(v)

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": organization_update_example},
    )

class OrganizationRead(OrganizationBase):
    """Schema for reading organization data."""
    org_id: UUID
    org_owner_id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": organization_read_example
        }
    )
