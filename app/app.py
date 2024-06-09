# Import the FastAPI framework
from fastapi import FastAPI

# Import routers from different modules
from app.routes.users_router import router as user_router
from app.routes.login_router import router as login_router
from app.routes.batch_routes import router as batch_router

# Create an instance of FastAPI
app = FastAPI()

# Include user_router with a prefix of "/user"
app.include_router(user_router, prefix="/user")

# Include login_router with a prefix of "/auth"
app.include_router(login_router, prefix="/auth")

# Include batch_router with a prefix of "/batch"
app.include_router(batch_router, prefix="/batch")
