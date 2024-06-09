from fastapi import APIRouter, Depends
from app.database.database import get_db
from app.models.users_models import users
from app.schemas.users_schemas import User
from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from cryptography.fernet import Fernet

key = Fernet_key = Fernet.generate_key()
f = Fernet(key)

router = APIRouter()

@router.get("/get_all_users")
def get_all_users(db: Session = Depends(get_db)):
    try:
        query = db.execute(users.select().where(users.c.status == 1)).all()
        data = []
        for row in query:
            data.append({
                "id": row.id,
                "email": row.email,
                "status": row.status
            })
        return {"status_code": HTTP_200_OK, "message": "Users found", "data": data}
    except SQLAlchemyError as e:
        return {"status_code": HTTP_400_BAD_REQUEST, "message": str(e)}

@router.get("/get_user/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
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
        new_user = {
            "email": user.email,
            "password": f.encrypt(user.password.encode("utf-8"))
        }
        result = db.execute(
            users.insert(                
            ).values(
                new_user
            )
        )
        db.commit()
        return {"status_code": HTTP_201_CREATED, "message": "User created successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"status_code": HTTP_400_BAD_REQUEST, "message": str(e)}
    

@router.put("/delete_user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
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
def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
    try:
        query = db.execute(
            users.update(
            ).where(
                users.c.id == user_id
            ).values(
                email=user.email,
                password=f.encrypt(user.password.encode("utf-8"))
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
