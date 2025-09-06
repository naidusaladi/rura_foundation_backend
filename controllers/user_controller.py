from fastapi import HTTPException
from models.user import new_user, user_helper
from schemas.user import UserCreate, UserLogin
from services.auth_service import hash_password, verify_password, create_access_token
from config.database import get_user_collection

user_collection = get_user_collection()  

async def register_user(user: UserCreate):
    existing_user = user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail={"status": "error", "message": "Email already registered", "body": None}
        )
    
    user_doc = new_user(
        user_name=user.user_name,
        email=user.email,
        password=hash_password(user.password),
        college=user.college,
        role=user.role
    )
    user_collection.insert_one(user_doc)
    
    return {
        "status": "success",
        "message": "User registered successfully",
        "body": {"email": user.email, "user_name": user.user_name}
    }

async def login_user(user: UserLogin):
    db_user = user_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=401,
            detail={"status": "error", "message": "Invalid email or password", "body": None}
        )
    
    token = create_access_token({"sub": db_user["email"], "role": db_user["role"]})
    return {
        "status": "success",
        "message": "Login successful",
        "body": {"access_token": token, "token_type": "bearer"}
    }
