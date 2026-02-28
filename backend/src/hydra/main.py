from fastapi import FastAPI

app = FastAPI()


@app.get("/hello")
async def get_greeting() -> dict[str, str]:
    return {"message": "Hello from hydra auth backend!"}
