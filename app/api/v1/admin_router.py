from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from app.models import User, UserRole
from app.schemas import UserRead
from .dependancies import db_dependancy, is_admin


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/", response_model=UserRead, status_code=status.HTTP_200_OK)
async def read_admin_root(
    db: db_dependancy, current_user: UserRead = Depends(is_admin)
) -> UserRead:
    return current_user


@router.get("/users/{username}", status_code=status.HTTP_200_OK)
async def admin_get_users_by_username(
    username: str, db: db_dependancy, current_user: UserRead = Depends(is_admin)
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return UserRead.model_validate(user)


@router.get("/users/user_email/{email}")
async def admin_get_users_by_email(
    email: EmailStr, db: db_dependancy, current_user: UserRead = Depends(is_admin)
):
    user = db.query(User).filter(User.email == email.strip().lower()).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return UserRead.model_validate(user)


@router.get("/users", status_code=status.HTTP_200_OK)
async def get_all_users(db: db_dependancy, current_user: UserRead = Depends(is_admin)):
    users = db.query(User).all()
    return [UserRead.model_validate(user) for user in users]
