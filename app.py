from fastapi import FastAPI,  Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from datetime import datetime
from database import connect_db
from fastapi import HTTPException
from datetime import datetime, timedelta
import random
from bson import ObjectId
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

db_name = 'hw'
collection = 'tasks'

def preprocess_task(task: dict):
    task['id'] = str(task['_id'])
    del task['_id']
    return task

# Endpoints for CRUD operations
@app.post("/create_task")
async def create_task(request: Request):
    data = await request.json()
    try:
        client = connect_db()
        db = client[db_name]  # Replace with your database name
        tasks_collection = db.get_collection(collection)

        task_data = {
            "title": data['title'],
            "author": data['author'],
            "description": data['description'],
            "deadline": data['deadline'],
        }
        print(f'Creating task {task_data}')

        # Insert the task into the collection
        result = tasks_collection.insert_one(task_data)
        if not result.inserted_id:
            raise HTTPException(status_code=400, detail="Failed to create task")

        created_task = tasks_collection.find_one(result.inserted_id)  # Convert to string before using in query
        created_task = preprocess_task(created_task)
        print(f'Task successfully created (ID: {result.inserted_id}): {created_task}')
        return created_task

    except Exception as e:
        print(f"Error creating task: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/tasks")
async def get_all_tasks():
    try:
        client = connect_db()
        db = client[db_name]
        tasks_collection = db.get_collection(collection)

        # Find all tasks in the collection
        tasks_list = []
        tasks = tasks_collection.find()
        for task in tasks:
            task = preprocess_task(task)
            tasks_list.append(task)

        return tasks_list

    except Exception as e:
        print(f"Error retrieving tasks: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/tasks/{task_id}")
async def get_task_by_id(task_id: str, request: Request):
    try:
        client = connect_db()
        db = client[db_name]  # Replace with your database name
        tasks_collection = db.get_collection(collection)

        object_id = ObjectId(task_id)
        task = tasks_collection.find_one({"_id": object_id})
        if not task:
            raise HTTPException(status_code=404, detail=f"Task (ID: {task_id}) not found")

        print(f'Task successfully retrieved (ID: {task_id}): {task}')

        task = preprocess_task(task)

        return templates.TemplateResponse(
            request=request, name="task-details.html", context={"request": request,
                                                                "task": task}
        )

    except Exception as e:
        print(f"Error retrieving task: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/tasks/{task_id}")
async def update_task(task_id: str, updated_data: dict = None):
    print(task_id, updated_data)
    try:
        client = connect_db()
        db = client[db_name]  # Replace with your database name
        tasks_collection = db.get_collection(collection)

        object_id = ObjectId(task_id)

        # Find the task to update
        task = tasks_collection.find_one({"_id": object_id})
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        # Update task data
        for key, value in updated_data.items():
            task[key] = value

        # Update the task in the collection
        update_result = tasks_collection.update_one({"_id": object_id}, {"$set": task})

        # Optionally, retrieve the updated task document
        updated_task = tasks_collection.find_one({"_id": object_id})

        updated_task = preprocess_task(updated_task)
        print(f'Task successfully updated (ID: {task_id}): {updated_task}')
        return updated_task

    except Exception as e:
        print(f"Error updating task: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)