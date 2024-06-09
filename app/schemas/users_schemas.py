from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id : Optional[int] = None 
    email : str
    password : str
    status : Optional[int] = 1