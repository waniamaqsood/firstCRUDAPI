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

# -------------------------
# CREATE task
# -------------------------

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_item(title: str, done: bool):

    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO tasks (title, done)
        VALUES (?, ?)
    """, (title, done))

    connection.commit()

    new_id = cursor.lastrowid

    connection.close()

    return {
        "id": new_id,
        "title": title,
        "done": done
    }


# -------------------------
# UPDATE task
# -------------------------

@app.put("/tasks/{id}")
def update_item(id: int, title: str, done: bool):

    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE tasks
        SET title = ?, done = ?
        WHERE id = ?
    """, (title, done, id))

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    connection.close()

    return {
        "id": id,
        "title": title,
        "done": done
    }


# -------------------------
# DELETE task
# -------------------------

@app.delete(
    "/tasks/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_item(id: int):

    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM tasks
        WHERE id = ?
    """, (id,))

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    connection.close()

# -------------------------
# GET task by done status
# -------------------------

@app.get("/tasks")
def get_item(done: bool):

    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, done
        FROM tasks
        WHERE done = ?
    """, (done,))

    rows = cursor.fetchall()

    connection.close()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return rows

