from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URL)
db = client["users_db"]

def get_user_collection():
    return db["users"]

def get_course_collection():
    return db["courses"]

def get_module_collection():
    return db["modules"]

def get_chapter_collection():
    return db["chapters"]
