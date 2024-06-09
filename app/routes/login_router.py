from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from app.models.users_models import users
from app.database.database import get_db
from app.schemas.users_schemas import User
from jose import jwt, JWTError
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from app.utils.security import verify_password

router = APIRouter()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create an access token using the provided data and expiration delta.

    Args:
        data (dict): The data to be encoded in the token.
        expires_delta (timedelta, optional): The expiration delta for the token. Defaults to None.

    Returns:
        str: The encoded access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/login")
def login(credentials: User, db: Session = Depends(get_db)):
    """
    Endpoint for user login.

    Args:
        credentials (User): The user credentials.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: The login response.
    """
    try:
        query = db.execute(
            users.select().where(users.c.email == credentials.email)
        ).first()

        if query and verify_password(credentials.password, query.password):
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(data={"sub": query.email}, expires_delta=access_token_expires)
            return {"status_code": HTTP_200_OK, "message": "Login successful", "access_token": access_token}
        else:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    except SQLAlchemyError as e:
        return {"status_code": HTTP_400_BAD_REQUEST, "message": str(e)}

def get_token(authorization: str = Header(...)):
    """
    Get the token from the authorization header.

    Args:
        authorization (str): The authorization header.

    Returns:
        str: The token.
    
    Raises:
        HTTPException: If the token is invalid.
    """
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split("Bearer ")[1]
        return token
    else:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")

def authenticate_token(token: str = Depends(get_token)):
    """
    Authenticate the token.

    Args:
        token (str): The token.

    Returns:
        str: The email associated with the token.
    
    Raises:
        HTTPException: If the token is invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email:
            return email
        else:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")
