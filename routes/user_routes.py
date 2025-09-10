from fastapi import APIRouter
from schemas.user import UserCreate, UserLogin
from controllers.user_controller import register_user, login_user, get_user_by_email

from urllib.parse import unquote

router = APIRouter(tags=["Users"])

@router.get("/{email}")
async def get_user_by_email_route(email: str):
    decoded_email = unquote(email)
    print(f"Decoded email in route: {decoded_email}")
    return await get_user_by_email(decoded_email)

@router.post("/register")
async def register(user: UserCreate):
    return await register_user(user)

@router.post("/login")
async def login(user: UserLogin):
    return await login_user(user)
