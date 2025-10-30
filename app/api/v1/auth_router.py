from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import UserCreate
from app.models import User
from starlette import status
from passlib.context import CryptContext
from pydantic import EmailStr
from .jwt_handler import create_access_token, create_refresh_token, verify_token
from .dependancies import db_dependancy , get_current_user


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated ='auto')


router = APIRouter(prefix="/auth")

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user_create:UserCreate, db:db_dependancy):
    user_model = User(
        first_name = user_create.first_name,
        last_name = user_create.last_name,
        username = user_create.username,
        email = user_create.email,
        hashed_password = bcrypt_context.hash(user_create.password)     
    )

    db.add(user_model)
    db.commit()

@router.get("/users", status_code=status.HTTP_200_OK)
async def get_users(db:db_dependancy, current_user: User = Depends(get_current_user)):
    if current_user.role == "ADMIN":
        users = db.query(User).all()
        return users
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

@router.get("/users/{username}", status_code=status.HTTP_200_OK)
async def get_users_by_username(username:str, db:db_dependancy, current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.username == username).first()
    return user

@router.get("/users/user_email/{email}")
async def get_users_by_email(email:EmailStr, db:db_dependancy, current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.email == email).first()
    return user


@router.post("/token")
async def login( db:db_dependancy,  response:Response, form_data:OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not bcrypt_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    access_token = create_access_token(data={"sub":user.id})
    refresh_token = create_refresh_token(data={"sub":user.id})
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,  # set to False for local testing, True in production (HTTPS only)
        samesite="none",  # or 'lax' depending on your frontend setup
        max_age=60 * 60 * 24 * 7  # 7 days
    )    

    return {
        "access_token":access_token,
        "token_type": "bearer"
    }



@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_access_token(
    db: db_dependancy,
    refresh_token: str | None = Cookie(default=None)
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

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "Successfully logged out"}