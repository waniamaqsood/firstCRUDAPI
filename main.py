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

@app.get("/api/tasks", response_model=List[Item])
def get_all_tasks():
    return task_db

@app.get("/api/tasks/{id}", response_model=Item)
def get_item(id: int):
    item = next((i for i in task_db if i["id"] == id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Task not found")
    return item

@app.post("/api/tasks", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
    new_id = max([i["id"] for i in task_db], default=0) + 1
    new_item = {"id": new_id, "title": item.title, "done": item.done}
    task_db.append(new_item)
    return new_item
