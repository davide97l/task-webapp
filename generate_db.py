from task_generator import generate_random_task
from database import connect_db
import asyncio

db_name = 'hw'
collection = 'tasks'

async def create_database_and_collection():
    try:
        client = connect_db()
        db = client[db_name]
        col = db[collection]
        print(f"Database '{db.name}' and collection '{collection}' created (if they didn't exist).")

    except Exception as e:
        print(f"Error creating database or collection: {e}")


async def insert_random_tasks(num_tasks=1):
    try:
        client = connect_db()
        db = client[db_name]
        tasks_collection = db.get_collection(collection)

        # Generate random tasks
        tasks = [generate_random_task() for _ in range(num_tasks)]

        # Insert tasks into the collection
        result = tasks_collection.insert_many(tasks)
        print(f"Successfully inserted {len(result.inserted_ids)} tasks!")

    except Exception as e:
        print(f"Error inserting tasks: {e}")


if __name__ == '__main__':
    asyncio.run(create_database_and_collection())
    asyncio.run(insert_random_tasks(3))
