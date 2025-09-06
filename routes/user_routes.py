from fastapi import APIRouter
from schemas.user import UserCreate, UserLogin
from controllers.user_controller import register_user, login_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
async def register(user: UserCreate):
    return await register_user(user)

@router.post("/login")
async def login(user: UserLogin):
    return await login_user(user)
