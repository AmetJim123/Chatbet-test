from fastapi import FastAPI
from app.routes.users_router import router as user_router

app = FastAPI()

app.include_router(user_router, prefix="/user")
