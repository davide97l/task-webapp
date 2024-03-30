from fastapi import FastAPI,  Request
from pydantic import BaseModel
from datetime import datetime
from database import connect_db
from fastapi import HTTPException
from datetime import datetime, timedelta
import random

app = FastAPI()

db_name = 'hw'
collection = 'tasks'

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
        print(f'Task successfully created (ID: {result.inserted_id})')

        created_task = tasks_collection.find_one(result.inserted_id)  # Convert to string before using in query
        del created_task['_id']
        return created_task

    except Exception as e:
        print(f"Error creating task: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/tasks")
async def get_all_tasks():
    # Logic to retrieve all tasks from database and return them as a list
    ...

@app.get("/tasks/{task_id}")
async def get_task_by_id(task_id: int):
    # Logic to retrieve a specific task by ID and return it
    ...

@app.put("/tasks/{task_id}")
async def update_task(task_id: int):
    # Logic to update a specific task based on ID and return the updated task
    ...


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)