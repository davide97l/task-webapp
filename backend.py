from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class Task(BaseModel):
    id: int | None = None
    title: str
    description: str | None = None
    author: str | None = None
    deadline: datetime | None = None
    completed: bool = False

# Endpoints for CRUD operations
@app.post("/tasks")
async def create_task(task: Task):
    # Logic to insert task into database and return the created task
    ...

@app.get("/tasks")
async def get_all_tasks():
    # Logic to retrieve all tasks from database and return them as a list
    ...

@app.get("/tasks/{task_id}")
async def get_task_by_id(task_id: int):
    # Logic to retrieve a specific task by ID and return it
    ...

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task: Task):
    # Logic to update a specific task based on ID and return the updated task
    ...
