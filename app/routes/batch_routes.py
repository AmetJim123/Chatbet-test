from typing import List
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database.database import get_db
from app.schemas.users_schemas import User, UserCreate, UserUpdate, UserId
from app.models.users_models import users
from app.utils.security import hash_password
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
import time
from app.routes.users_router import create_user, get_user, update_user, delete_user

router = APIRouter()

def process_users_batch(users_data: List, process_func, db: Session):
    try:
        start_time = time.time()
        for user_data in users_data:
            process_func(user_data, db)
            if time.time() - start_time > 10:
                print("Batch processing took longer than 10 seconds")
                break
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error during batch processing: {e}")


@router.post("/webhook/create_users_batch")
async def webhook_create_users_batch(users_data: List[UserCreate], backgroud_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    backgroud_tasks.add_task(process_users_batch, users_data, create_user, db)
    return {"message": "Batch processing initiated"}

@router.put("/webhook/update_users_batch")
async def webhook_update_users_batch(users_data: List[UserUpdate], backgroud_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    backgroud_tasks.add_task(process_users_batch, users_data, update_user, db)
    return {"message": "Batch processing initiated"}

@router.put("/webhook/delete_users_batch")
async def webhook_delete_users_batch(users_data: List[UserId], backgroud_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    backgroud_tasks.add_task(process_users_batch, users_data, delete_user, db)
    return {"message": "Batch processing initiated"}
