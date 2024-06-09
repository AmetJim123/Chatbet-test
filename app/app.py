from fastapi import FastAPI
from app.routes.users_router import router as user_router
from app.routes.login_router import router as login_router

app = FastAPI()

app.include_router(user_router, prefix="/user")
app.include_router(login_router, prefix="/auth")