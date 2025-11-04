from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.schemas import TodoCreate, TodoRead, UserRead
from app.models import Todo, User
from starlette import status
from .dependancies import db_dependancy , get_current_user

router = APIRouter(prefix="/todos" ,tags=["Todos"])

@router.get("/", response_model=List[TodoRead])
async def get_todo_list(db:db_dependancy ,user:UserRead=Depends(get_current_user)):
    if user:
        todo_list = db.query(Todo).filter(Todo.owner_id == str(user.id)).all()
        return todo_list
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)



@router.post("/create_todo", response_model=TodoRead)
async def create_todo(todo:TodoCreate, db:db_dependancy, user:UserRead=Depends(get_current_user)):
    todo_model = Todo(
        **todo.model_dump(),
        owner_id=str(user.id)  # <-- important! Sqlite saves the owner_id as string
    )
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model
