import os
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv('URI_MONGO')

# Create a new client and connect to the server
conn = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    conn.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
