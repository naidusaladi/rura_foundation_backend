from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URL = os.getenv("MONGO_URI")
print(MONGO_URL)
def get_user_collection():
    client = MongoClient(MONGO_URL)
    db = client["users_db"]
    return db["users"]

