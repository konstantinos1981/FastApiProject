from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from app.models import User, UserRole
from app.schemas import UserRead
from .dependancies import db_dependancy, get_current_user


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/", response_model=UserRead, status_code=status.HTTP_200_OK)
async def read_admin_root(
    db: db_dependancy, 
    current_user: User = Depends(get_current_user)
) -> UserRead:
    # Compare using enum values to ensure correct matching
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can access this endpoint"
        )
    
    return current_user

@router.get("/users/{username}", status_code=status.HTTP_200_OK)
async def admin_get_users_by_username( username:str, db:db_dependancy, current_user: User = Depends(get_current_user)):
    if current_user.role == UserRole.admin:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserRead.model_validate(user)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


@router.get("/users/user_email/{email}")
async def admin_get_users_by_email(email:EmailStr, db:db_dependancy, current_user: User = Depends(get_current_user)):
    if current_user.role == UserRole.admin:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserRead.model_validate(user)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


@router.get("/users", status_code=status.HTTP_200_OK)
async def get_all_users(db:db_dependancy, current_user: User = Depends(get_current_user)):
    if current_user.role == UserRole.admin:
        users = db.query(User).all()
        return [UserRead.model_validate(user) for user in users]
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")