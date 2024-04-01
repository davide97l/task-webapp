import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from bson import ObjectId
import uvicorn
from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv
import os
from datetime import date
from typing import Optional

from database import get_tasks_collection, get_db_client

load_dotenv()

app = FastAPI()
app.title = "Tasks Manager"
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

SERVER_PORT = int(os.getenv("SERVER_PORT"))

logging.basicConfig(level=logging.INFO)


class TaskModel(BaseModel):
    title: str = Field(..., min_length=1, max_length=30)
    author: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[str] = None  # "Deadline in YYYY-MM-DD format"

    @validator("deadline")
    def validate_deadline_format(cls, value):
        try:
            date.fromisoformat(str(value))  # Convert to string for parsing
            return value
        except ValueError:
            raise ValueError("Invalid deadline format. Use YYYY-MM-DD")

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
    """
    Preprocess a task dictionary to replace '_id' key with 'id'.

    Args:
        task (dict): The task dictionary to preprocess.

    Returns:
        dict: The preprocessed task dictionary.
    """
    task['id'] = str(task['_id'])
    del task['_id']
    return task


@app.post("/create_task", status_code=201)
async def create_task(task: TaskModel) -> dict:
    """
    Create a new task.

    Args:
        request (Request): The request object.
        task (TaskModel): The task data.

    Returns:
        dict: The created task.
    """
    try:
        tasks_collection = get_tasks_collection(get_db_client())
        task_data = task.dict()

        result = tasks_collection.insert_one(task_data)

        if not result.inserted_id:
            raise HTTPException(status_code=400, detail="Failed to create task")

        created_task = preprocess_task(tasks_collection.find_one(result.inserted_id))
        logging.info(f'Task successfully created: {created_task}')
        return created_task

    except Exception as e:
        logging.error(f"Failed to create task: {e}")
        raise HTTPException(status_code=500, detail="Failed to create task")


@app.get("/tasks", status_code=200)
async def get_all_tasks() -> list:
    """
    Get all tasks.

    Returns:
        list: The list of all tasks.
    """
    try:
        tasks_collection = get_tasks_collection(get_db_client())
        tasks_list = [preprocess_task(task) for task in tasks_collection.find()]
        logging.debug(f'Retrieved tasks: {tasks_list}')
        return tasks_list
    except Exception as e:
        logging.error(f"Failed to retrieve tasks: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve tasks")


@app.get("/tasks/{task_id}", status_code=200)
async def get_task_by_id(task_id: str, request: Request) -> dict:
    """
    Get a task by its ID.

    Args:
        task_id (str): The ID of the task.
        request (Request): The request object.

    Returns:
        dict: The task data.
    """
    try:
        tasks_collection = get_tasks_collection(get_db_client())
        task = tasks_collection.find_one({"_id": ObjectId(task_id)})
        if not task:
            raise HTTPException(status_code=404, detail=f"Task (ID: {task_id}) not found")

        task = preprocess_task(task)
        logging.info(f'Task successfully retrieved: {task}')
        return templates.TemplateResponse(
            request=request, name="task-details.html", context={"request": request, "task": task}
        )
    except Exception as e:
        logging.error(f"Failed to retrieve task: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve task")


@app.put("/tasks/{task_id}", status_code=200)
async def update_task(task_id: str, updated_data: TaskModel) -> dict:
    """
    Update a task.

    Args:
        task_id (str): The ID of the task.
        updated_data (TaskModel): updated task data

    Returns:
        dict: The updated task data.
    """
    try:
        tasks_collection = get_tasks_collection(get_db_client())

        # Find the task to update
        task = tasks_collection.find_one({"_id": ObjectId(task_id)})
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        # Update task data
        updated_data = updated_data.dict()
        task.update(updated_data)

        # Update the task in the collection
        tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": task})

        # Optionally, retrieve the updated task document
        updated_task = preprocess_task(tasks_collection.find_one({"_id": ObjectId(task_id)}))
        logging.info(f'Task successfully updated: {updated_task}')
        return updated_task
    except Exception as e:
        logging.error(f"Failed to update task: {e}")
        raise HTTPException(status_code=500, detail="Failed to update task")


@app.get("/", status_code=200)
async def index(request: Request):
    """
    Render the index page.

    Args:
        request (Request): The request object.

    Returns:
        TemplateResponse: The rendered index page.
    """
    context = {"request": request}
    return templates.TemplateResponse("index.html", context=context)


if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=SERVER_PORT, reload=True)
