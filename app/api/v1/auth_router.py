from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import UserCreate
from app.models import User, UserRole
from starlette import status
from passlib.context import CryptContext
from pydantic import EmailStr

from app.schemas.user_schema import UserRead
from .jwt_handler import create_access_token, create_refresh_token, verify_token
from .dependancies import db_dependancy, get_current_user


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/token")
async def login(
    db: db_dependancy,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if (
        not user
        or not bcrypt_context.verify(form_data.password, user.hashed_password)
        or not (form_data.username == user.display_name)
    ):
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,  # set to False for local testing, True in production (HTTPS only)
        samesite="none",  # or 'lax' depending on your frontend setup
        max_age=60 * 60 * 24 * 7,  # 7 days
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_access_token(
    db: db_dependancy, refresh_token: str | None = Cookie(default=None)
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    payload = verify_token(refresh_token, refresh=True)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_access_token = create_access_token(data={"sub": user.id})

    return {"access_token": new_access_token, "token_type": "bearer"}
