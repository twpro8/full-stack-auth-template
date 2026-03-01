from fastapi import FastAPI

from hydra.config import settings
from hydra.api import master_router

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(master_router, prefix=settings.API_V1_STR)


@app.get("/hello")
async def get_greeting() -> dict[str, str]:
    return {"message": "Hello from hydra auth backend!"}
