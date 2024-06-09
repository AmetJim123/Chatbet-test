from fastapi import APIRouter, Depends, Body
from app.database.database import get_db
from app.models.users_models import users
from app.schemas.users_schemas import User
from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from app.utils.security import hash_password
from .login_router import authenticate_token
import re



router = APIRouter()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

DEFAULT_PAGE_SIZE = 10

@router.get("/get_all_users")
def get_all_users(data: dict = Body(...), db: Session = Depends(get_db), token: str = Depends(authenticate_token)):

    page = data.get("page", 1)
    page_size = data.get("page_size", DEFAULT_PAGE_SIZE)

    try:
        offset = (page - 1) * page_size
        query = db.execute(users.select().where(users.c.status == 1).offset(offset).limit(page_size)).all()
        data = []
        for row in query:
            data.append({
                "id": row.id,
                "email": row.email,
                "status": row.status
            })
        if len(data) == 0:
            return {"status_code": HTTP_404_NOT_FOUND, "message": "No users found"}
        return {"status_code": HTTP_200_OK, "message": "Users found", "data": data}
    
    except SQLAlchemyError as e:
        return {"status_code": HTTP_400_BAD_REQUEST, "message": str(e)}

@router.get("/get_user/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(authenticate_token)):
    try:
        query = db.execute(users.select().where(and_(users.c.id == user_id, users.c.status == 1))).first()
        if query:
            data = {
                "id": query.id,
                "email": query.email,
                "status": query.status
            }
            return {"status_code": HTTP_200_OK, "message": "User found", "data": data}
        else:
            return {"status_code": HTTP_404_NOT_FOUND, "message": "User not found"}
    except SQLAlchemyError as e:
        return {"status_code": HTTP_400_BAD_REQUEST, "message": str(e)}


@router.post("/create_user")
def create_user(user: User, db: Session = Depends(get_db)):
    try:

        if not EMAIL_REGEX.match(user.email):
            return {"status_code": HTTP_400_BAD_REQUEST, "message": "Invalid email address"}

        new_user = {
            "email": user.email,
            "password": hash_password.hash(user.password)  # Use hash() method instead of calling the CryptContext object
        }
        result = db.execute(
            users.insert(                
            ).values(
                new_user
            ).returning(users.c.id)
        )
        db.commit()
        user_id = result.fetchone()[0]
        return {"status_code": HTTP_201_CREATED, "message": "User created successfully"}
    except IntegrityError as e:
        db.rollback()
        return {"status_code": HTTP_400_BAD_REQUEST, "message": "Email already exists"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"status_code": HTTP_400_BAD_REQUEST, "message": str(e)}
    

@router.put("/delete_user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(authenticate_token)):
    try:
        query = db.execute(users.update().where(users.c.id == user_id).values(status=0))
        db.commit()
        if query.rowcount > 0:
            return {"status_code": HTTP_204_NO_CONTENT, "message": "User deleted successfully"}
        else:
            return {"status_code": HTTP_404_NOT_FOUND, "message": "User not found"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"status_code": HTTP_400_BAD_REQUEST, "message": str(e)}

@router.put("/update_user/{user_id}")
def update_user(user_id: int, user: User, db: Session = Depends(get_db), token: str = Depends(authenticate_token)):
    try:
        query = db.execute(
            users.update().where(users.c.id == user_id).values(
                email=user.email,
                password=hash_password.hash(user.password)  # Use hash() method instead of calling the CryptContext object
            )
        )
        db.commit()
        if query.rowcount > 0:
            return {"status_code": HTTP_200_OK, "message": "User updated successfully"}
        else:
            return {"status_code": HTTP_404_NOT_FOUND, "message": "User not found"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"status_code": HTTP_400_BAD_REQUEST, "message": str(e)}
