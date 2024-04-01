from task_generator import generate_random_task
import asyncio
from database import get_tasks_collection, get_db_client, connect_db, DB_NAME, COLLECTION

db_name = 'hw'
collection = 'tasks'


async def create_database_and_collection():
    try:
        db = get_db_client()
        collection = get_tasks_collection(db)
        print(f"Database '{DB_NAME}' and collection '{COLLECTION}' created (if they didn't exist).")

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


# Run to populate DB with 3 random tasks
if __name__ == '__main__':
    asyncio.run(create_database_and_collection())
    asyncio.run(insert_random_tasks(3))
