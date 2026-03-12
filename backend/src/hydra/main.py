from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from hydra.config import settings
from hydra.api import master_router
from hydra.errors import HydraError, app_exception_handler

app = FastAPI(title=settings.PROJECT_NAME)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALL_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(HydraError, app_exception_handler)  # type: ignore
app.include_router(master_router, prefix=settings.API_V1_STR)


@app.get("/hello")
async def get_greeting() -> dict[str, str]:
    return {"message": "Hello from hydra auth backend!"}
