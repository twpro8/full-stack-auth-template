from fastapi import APIRouter

from hydra.api.routes import auth, user

master_router = APIRouter()
master_router.include_router(auth.router)
master_router.include_router(user.router)
