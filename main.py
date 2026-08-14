from fastapi import FastAPI, HTTPException, status, Response, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator
from typing import List

app = FastAPI(
    title="Task API",
    description="A simple in-memory CRUD API",
    version="1.0.0"
)

class Item(BaseModel):
    id: int
    title: str
    done: bool


class ItemCreate(BaseModel):
    title: str
    done: bool

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str):
        if not value.strip():
            raise ValueError("title cannot be empty")
        return value

task_db = [
    {"id": 1, "title": "Task One", "done": True},
    {"id": 2, "title": "Task Two", "done": False},
    {"id": 3, "title": "Task Three", "done": True},
]


# -------------------------
# Error handling
# -------------------------

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Invalid request body"
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail
        }
    )

@app.get("/")
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": [
            "/tasks",
            "/tasks/{id}"
        ]
    }


@app.get("/tasks", response_model=List[Item])
def get_all_tasks():
    return task_db


@app.get("/tasks/{id}", response_model=Item)
def get_item(id: int):

    item = next(
        (i for i in task_db if i["id"] == id),
        None
    )

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return item


@app.post(
    "/tasks",
    response_model=Item,
    status_code=status.HTTP_201_CREATED
)
def create_item(item: ItemCreate):

    new_id = max(
        [i["id"] for i in task_db],
        default=0
    ) + 1

    new_item = {
        "id": new_id,
        "title": item.title,
        "done": item.done
    }

    task_db.append(new_item)

    return new_item


@app.put("/tasks/{item_id}", response_model=Item)
def update_item(
    item_id: int,
    updated_item: ItemCreate
):

    item = next(
        (i for i in task_db if i["id"] == item_id),
        None
    )

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    item["title"] = updated_item.title
    item["done"] = updated_item.done

    return item

@app.delete(
    "/tasks/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_item(item_id: int):

    global task_db

    item = next(
        (i for i in task_db if i["id"] == item_id),
        None
    )

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    task_db = [
        i for i in task_db
        if i["id"] != item_id
    ]

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )