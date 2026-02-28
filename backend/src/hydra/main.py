from fastapi import FastAPI


app = FastAPI()


@app.get("/hello")
async def get_greeting():
    return {"message": "Hello from hydra auth backend!"}
