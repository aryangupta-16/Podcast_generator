from mongoengine import connect
from dotenv import load_dotenv

load_dotenv()

import os

# Load from environment variable for safety
MONGODB_URI = os.getenv("MONGODB_URI")

def init_db():
    connect(
        db="podcastGenerator", 
        host=MONGODB_URI,
    )

    print("Connected to MongoDB")

# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi

# uri = "mongodb+srv://guptaaryan1604_db_user:Qw6wIGPvABJgeOn6@podcastgenerator.voirbca.mongodb.net/?retryWrites=true&w=majority&appName=podcastGenerator"

# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))

# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

# python -m pip install "pymongo[srv]==3.12"