from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import EmailStr
from typing import List
from app.models import User
from app.schemas import UserRead
from app.schemas.todo_schema import TodoRead
from .dependancies import db_dependancy, is_admin


router = APIRouter(prefix="/admin", tags=["admin"])


def get_user(
    db: db_dependancy, username: str | None = None, email: EmailStr | None = None
) -> User:
    if email:
        user: User = db.query(User).filter(User.email == email.strip().lower()).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with email {email} not found",
            )
        return user
    if username:
        user: User = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {username} not found",
            )
        return user
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Either username or email must be provided",
    )


@router.get("/", response_model=UserRead, status_code=status.HTTP_200_OK)
async def read_admin_root(
    db: db_dependancy, current_user: dict = Depends(is_admin)
) -> UserRead:
    user_id = current_user.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    return UserRead.model_validate(user)


@router.get("/user/{username}", status_code=status.HTTP_200_OK)
async def admin_get_users_by_username(
    username: str, db: db_dependancy, current_user: UserRead = Depends(is_admin)
) -> UserRead:
    user = get_user(db=db, username=username)
    return UserRead.model_validate(user)


@router.get("/user/user_email/{email}")
async def admin_get_users_by_email(
    email: EmailStr, db: db_dependancy, current_user: UserRead = Depends(is_admin)
):
    user = get_user(db=db, email=email)
    return UserRead.model_validate(user)


@router.get("/users/all", status_code=status.HTTP_200_OK)
async def get_all_users(db: db_dependancy, current_user: UserRead = Depends(is_admin)):
    users = db.query(User).all()
    return [UserRead.model_validate(user) for user in users]


@router.get("/user/{username}/todos", status_code=status.HTTP_200_OK)
async def get_all_user_todos_by_username(
    username: str, db: db_dependancy, current_user: UserRead = Depends(is_admin)
) -> List[TodoRead]:
    user = get_user(db=db, username=username)
    return [TodoRead.model_validate(todo) for todo in user.todos]


@router.get("/user/{username}/pending", status_code=status.HTTP_200_OK)
async def get_pending_todos_by_username(
    username: str, db: db_dependancy, current_user: UserRead = Depends(is_admin)
) -> List[TodoRead]:
    user = get_user(db=db, username=username)
    pending_todos = [todo for todo in user.todos if not todo.is_completed]
    return [TodoRead.model_validate(todo) for todo in pending_todos]
