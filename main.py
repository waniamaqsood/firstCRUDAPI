from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="FastAPI CRUD API",
    description="A simple CRUD API",
    version="1.0.0"
)

class Item(BaseModel):
    id: int
    title: str 
    done: bool

class ItemCreate(BaseModel):
    title: str 
    done: bool

task_db = [
    {"id": 1, "title": "Task One", "done": True},
    {"id": 2, "title": "Task Two", "done": False},
    {"id": 3, "title": "Task Three", "done": True},
]

@app.get("/") 
def read_root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/api/tasks"] }