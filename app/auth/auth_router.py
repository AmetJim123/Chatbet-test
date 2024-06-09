# app/auth/auth_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.models.users import User
from app.auth.jwt_utils import create_access_token, verify_password, get_password_hash

fake_users_db = {
    "user@example.com": {
        "email": "user@example.com",
        "password": get_password_hash("password123")
    }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str

def authenticate_user(fake_db, email: str, password: str):
    user = fake_db.get(email)
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return User(**user)

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
