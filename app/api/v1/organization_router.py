from fastapi import APIRouter, Depends, HTTPException, Response
from app.schemas import (
    OrganizationRead,
    OrganizationCreate,
    OrganizationUpdate,
)
from app.models import User, Organization
from .dependancies import db_dependancy, get_current_user, get_organization, is_admin
from starlette import status
from .jwt_handler import create_access_token, create_refresh_token

router = APIRouter(prefix="/organization", tags=["Organization"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user_organization(
    db: db_dependancy, org_payload: dict = Depends(get_organization)
) -> OrganizationRead:
    org_id = org_payload.get("org")  # Extract the org_id from JWT

    organization = (
        db.query(Organization)
        .filter(Organization.org_id == org_id)  # Filter by org_id, not org_name
        .first()
    )

    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    return OrganizationRead.model_validate(organization)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_organization(
    db: db_dependancy,
    response: Response,
    organization_create: OrganizationCreate,
    current_user: dict = Depends(is_admin),
):

    organization_model = Organization(
        **organization_create.model_dump(),
        org_owner_id=current_user.get("sub"),
    )

    db.add(organization_model)
    db.commit()

    # Update the user's organization_id
    user_id = current_user.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.organization_id = organization_model.org_id
    db.commit()
    db.refresh(user)
    # Generate new tokens with updated org_id

    new_access_token = create_access_token(
        data={
            "sub": user.id,
            "org": user.organization_id,  # Now includes the org_id
            "role": user.role.value,
        }
    )
    new_refresh_token = create_refresh_token(
        data={"sub": user.id, "org": user.organization_id, "role": user.role.value}
    )

    # Update the refresh token cookie
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=60 * 60 * 24 * 7,
    )

    return {
        "message": f"Organization {organization_model.org_name} created successfully",
        "org_id": organization_model.org_id,
        "access_token": new_access_token,  # Return new token
        "token_type": "bearer",
    }


@router.put("/update", status_code=status.HTTP_200_OK)
async def update_organization(
    db: db_dependancy,
    organization_update: OrganizationUpdate,
    org_payload: dict = Depends(get_organization),
):
    org_id = org_payload.get("org")

    organization = (
        db.query(Organization).filter(Organization.org_id == org_id).first()
    )

    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    for key, value in organization_update.model_dump(exclude_unset=True).items():
        setattr(organization, key, value)

    db.commit()
    db.refresh(organization)

    return OrganizationRead.model_validate(organization)  
