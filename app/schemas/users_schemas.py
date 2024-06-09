from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    """
    Represents a user.

    Attributes:
        id (Optional[int]): The user's ID.
        email (str): The user's email address.
        password (str): The user's password.
        status (Optional[int]): The user's status (default is 1).
    """
    id: Optional[int] = None 
    email: str
    password: str
    status: Optional[int] = 1

class UserCreate(BaseModel):
    """
    Represents a user creation request.

    Attributes:
        email (str): The user's email address.
        password (str): The user's password.
    """
    email: str
    password: str

class UserId(BaseModel):
    """
    Represents a user ID.

    Attributes:
        id (int): The user's ID.
    """
    id: int

class UserUpdate(BaseModel):
    """
    Represents a user update request.

    Attributes:
        id (int): The user's ID.
        email (Optional[str]): The user's updated email address.
        password (Optional[str]): The user's updated password.
    """
    id: int
    email: Optional[str] = None
    password: Optional[str] = None

class UserEmail(BaseModel):
    """
    Represents a user email.

    Attributes:
        email (str): The user's email address.
    """
    email: str
