#!app/main.py
from fastapi import FastAPI
import uvicorn
from app.api.v1.routers.task import task_router


app = FastAPI()

app.include_router(router=task_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
