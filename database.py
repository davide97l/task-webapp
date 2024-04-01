from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import logging
from fastapi import HTTPException
import os

load_dotenv()

#DB_NAME = 'hw'
#COLLECTION = 'tasks'
DB_NAME = os.getenv("DB_NAME")
COLLECTION = os.getenv("COLLECTION")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PWD = os.getenv("DB_PWD")
DB_CLUSTER = os.getenv("DB_CLUSTER")


def connect_db():
    uri = f"mongodb+srv://{DB_USERNAME}:{DB_PWD}@{DB_CLUSTER}/?retryWrites=true&w=majority&appName=Cluster0"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    return client


def get_db_client() -> object:
    """
    Get the database client object.

    Returns:
        object: The database client object.
    """
    try:
        return connect_db()[DB_NAME]
    except Exception as e:
        logging.error(f"Failed to connect to database: {e}")
        raise HTTPException(status_code=500, detail="Failed to connect to database")


def get_tasks_collection(db_client) -> object:
    """
    Get the tasks collection object.

    Args:
        db_client (object): The database client object.

    Returns:
        object: The tasks collection object.
    """

    try:
        return db_client.get_collection(COLLECTION)
    except Exception as e:
        logging.error(f"Failed to connect to collection: {e}")
        raise HTTPException(status_code=500, detail="Failed to get collection")


# Test if connection works
if __name__ == '__main__':
    client = connect_db()
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
