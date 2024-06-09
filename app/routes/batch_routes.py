from typing import List
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database.database import get_db
from app.schemas.users_schemas import User
from app.models.users_models import users
from app.utils.security import hash_password
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
import time

router = APIRouter()

def insert_user(user_data: User, db: Session):
    try:
        new_user = {
            "email": user_data.email,
            "password": hash_password.hash(user_data.password),
            "status": user_data.status
        }
        result = db.execute(
            users.insert().values(new_user)
        )
        db.commit()
        return result
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))


def process_users_batch(users_data: List[User], db: Session):
    try:
        start_time = time.time()
        for user_data in users_data:
            insert_user(user_data, db)
            if time.time() - start_time > 10:
                print("Batch processing took longer than 10 seconds")
                break
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error during batch processing: {e}")


@router.post("/webhook/create_users_batch")
async def webhook_create_users_batch(users_data: List[User], background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(process_users_batch, users_data, db)
    return {"message": "Batch processing initiated"}