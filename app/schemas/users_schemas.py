from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id : Optional[int] = None 
    email : str
    password : str
    status : Optional[int] = 1

class UserCreate(BaseModel):
    email : str
    password : str

class UserId(BaseModel):
    id : int

class UserUpdate(BaseModel):
    id : int
    email : Optional[str] = None
    password : Optional[str] = None

class UserEmail(BaseModel):
    email : str