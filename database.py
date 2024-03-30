from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

pwd = 'JecYohKcGZMAw1x0'
usr = 'davide97ls'

def connect_db():
    uri = f"mongodb+srv://{usr}:{pwd}@cluster0.mlq35sd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    return client


if __name__ == '__main__':
    client = connect_db()
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)