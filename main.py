from fastapi import FastAPI, HTTPException, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import sqlite3

app = FastAPI(
    title="Task API",
    description="A simple SQLite CRUD API",
    version="1.0.0"
)

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


# -------------------------
# Root
# -------------------------

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


# -------------------------
# GET all tasks
# -------------------------

@app.get("/tasks")
def get_all_tasks():

    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, done
        FROM tasks
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


# -------------------------
# GET one task
# -------------------------

@app.get("/tasks/{id}")
def get_item(id: int):

    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, done
        FROM tasks
        WHERE id = ?
    """, (id,))

    row = cursor.fetchone()

    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return row


