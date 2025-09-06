from datetime import datetime
from uuid import UUID, uuid4

def user_helper(user) -> dict:
    return {
        "user_id":user.get("user_id"),
        "user_name":user.get("user_name"),       
        "email":user.get("email"),
        "college":user.get("college"),
        "role":user.get("role"),
        "created_at":user.get("created_at"),
        "updated_at":user.get("updated_at")
    }

def new_user(user_name,email,password,college,role):
    user_id = str(uuid4())
    return {
        "user_id": user_id,
        "user_name": user_name,
        "email": email,
        "password": password,
        "college": college,
        "role": role,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
