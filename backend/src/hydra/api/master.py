from fastapi import APIRouter

from hydra.api.routes import auth

master_router = APIRouter()
master_router.include_router(auth.router)
