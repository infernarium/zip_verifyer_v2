#!app/main.py
from fastapi import FastAPI
from app.api.v1.routers.task import task_router


app = FastAPI()

app.include_router(router=task_router)
