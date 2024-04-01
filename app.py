import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from bson import ObjectId
import uvicorn
from typing import Optional
from pydantic import BaseModel, Field
from datetime import date

from database import connect_db

app = FastAPI()
app.title = "Tasks Manager"
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

DB_NAME = 'hw'
COLLECTION = 'tasks'

logging.basicConfig(level=logging.INFO)


class TaskModel(BaseModel):
    title: str = Field(..., min_length=1, max_length=30)
    author: Optional[str] = None
    description: Optional[str] = None
    deadline: str = None

    class Config:
        schema_extra = {
            "example": {
                "title": "My Task",
                "author": "Davide",
                "description": "This is a sample task",
                "deadline": "2022-12-31"
            }
        }


def preprocess_task(task: dict) -> dict:
    task['id'] = str(task['_id'])
    del task['_id']
    return task


def get_db_client() -> object:
    return connect_db()[DB_NAME]


def get_tasks_collection(db_client) -> object:
    return db_client.get_collection(COLLECTION)


@app.post("/create_task")
async def create_task(request: Request, task: TaskModel) -> dict:
    tasks_collection = get_tasks_collection(get_db_client())
    task_data = task.dict()

    result = tasks_collection.insert_one(task_data)
    if not result.inserted_id:
        raise HTTPException(status_code=400, detail="Failed to create task")

    created_task = preprocess_task(tasks_collection.find_one(result.inserted_id))
    logging.info(f'Task successfully created {created_task}')
    return created_task


@app.get("/tasks")
async def get_all_tasks() -> list:
    tasks_collection = get_tasks_collection(get_db_client())
    tasks_list = [preprocess_task(task) for task in tasks_collection.find()]
    logging.debug(f'Retrieved tasks: {tasks_list}')
    return tasks_list


@app.get("/tasks/{task_id}")
async def get_task_by_id(task_id: str, request: Request) -> dict:
    tasks_collection = get_tasks_collection(get_db_client())
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail=f"Task (ID: {task_id}) not found")

    task = preprocess_task(task)
    logging.info(f'Task successfully retrieved {task}')
    return templates.TemplateResponse(
        request=request, name="task-details.html", context={"request": request, "task": task}
    )


@app.put("/tasks/{task_id}")
async def update_task(task_id: str) -> dict:
    tasks_collection = get_tasks_collection(get_db_client())

    # Find the task to update
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update task data
    task.update(task.dict())

    # Update the task in the collection
    tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": task})

    # Optionally, retrieve the updated task document
    updated_task = preprocess_task(tasks_collection.find_one({"_id": ObjectId(task_id)}))
    logging.info(f'Task successfully updated {updated_task}')
    return updated_task


@app.get("/")
async def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context=context)


if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)