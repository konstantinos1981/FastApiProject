from fastapi import APIRouter, Depends, HTTPException, Response
from app.api.v1.auth_router import bcrypt_context
from app.schemas import UserUpdate, UserPasswordUpdate
from app.models import User
from .dependancies import db_dependancy , get_current_user
from starlette import status
from app.schemas.user_schema import UserCreate, UserRead

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/profile", status_code=status.HTTP_200_OK)
async def get_profile(db:db_dependancy, current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user.username).first()
    return UserRead.model_validate(user)

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
    return {"message": f"User {user_model.username} created successfully"}

@router.put("/update", status_code=status.HTTP_200_OK)
async def update_user(user_update:UserUpdate, db:db_dependancy, current_user:User = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_update.email and user_update.email != user.email:
        existing_email = db.query(User).filter(
            User.email == user_update.email,
            User.id != user.id
        ).first()
        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Email already in use"
            )
        if user_update.username and user_update.username != user.username:
            existing_username = db.query(User).filter(
            User.username == user_update.username,
            User.id != user.id
        ).first()
            if existing_username:
                raise HTTPException(
                    status_code=400,
                    detail="Username already in use"
                )
    if user_update.first_name is not None:
        user.first_name = user_update.first_name

    if user_update.last_name is not None:
        user.last_name = user_update.last_name

    if user_update.email is not None:
        user.email = user_update.email

    if user_update.username is not None:
        user.username = user_update.username

    try:
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error updating user") from e

    return UserRead.model_validate(user)


@router.delete("/delete", status_code=status.HTTP_200_OK)
async def delete_user(response:Response, db:db_dependancy, current_user: User = Depends(get_current_user) ):
    user = db.query(User).filter(User.username == current_user.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    response.delete_cookie("refresh_token")
    return {"message": f"User {current_user.username} deleted successfully"}


@router.put("/change_password", status_code=status.HTTP_200_OK)
async def change_password(password_update: UserPasswordUpdate, db: db_dependancy, current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt_context.verify(password_update.old_password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Old password is incorrect")

    if password_update.new_password != password_update.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    user.hashed_password = bcrypt_context.hash(password_update.new_password)
    db.commit()
    return {"message": "Password updated successfully"}
