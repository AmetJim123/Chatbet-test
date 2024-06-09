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
from app.routes.users_router import create_user, update_user, delete_user

router = APIRouter()

def process_users_batch(users_data: List, process_func, db: Session):
    """
    Process a batch of user data using the specified process function and database session.

    Parameters:
    - users_data (List): A list of user data to be processed.
    - process_func (function): The function to be used for processing each user data.
    - db (Session): The database session to be used for database operations.

    Returns:
    None
    """
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
    """
    Endpoint for creating users in batch using a webhook.

    Parameters:
    - users_data (List[UserCreate]): A list of user data to be created.
    - backgroud_tasks (BackgroundTasks): Background tasks to be executed.
    - db (Session): The database session to be used for database operations.

    Returns:
    - dict: A dictionary with a message indicating that batch processing has been initiated.
    """
    backgroud_tasks.add_task(process_users_batch, users_data, create_user, db)
    return {"message": "Batch processing initiated"}

@router.put("/webhook/update_users_batch")
async def webhook_update_users_batch(users_data: List[UserUpdate], backgroud_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Endpoint for updating users in batch using a webhook.

    Parameters:
    - users_data (List[UserUpdate]): A list of user data to be updated.
    - backgroud_tasks (BackgroundTasks): Background tasks to be executed.
    - db (Session): The database session to be used for database operations.

    Returns:
    - dict: A dictionary with a message indicating that batch processing has been initiated.
    """
    backgroud_tasks.add_task(process_users_batch, users_data, update_user, db)
    return {"message": "Batch processing initiated"}

@router.put("/webhook/delete_users_batch")
async def webhook_delete_users_batch(users_data: List[UserId], backgroud_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Endpoint for deleting users in batch using a webhook.

    Parameters:
    - users_data (List[UserId]): A list of user IDs to be deleted.
    - backgroud_tasks (BackgroundTasks): Background tasks to be executed.
    - db (Session): The database session to be used for database operations.

    Returns:
    - dict: A dictionary with a message indicating that batch processing has been initiated.
    """
    backgroud_tasks.add_task(process_users_batch, users_data, delete_user, db)
    return {"message": "Batch processing initiated"}
