from pydantic import BaseModel, EmailStr, Field
from typing import Optional 
from datetime import datetime
from uuid import UUID, uuid4

class UserBase(BaseModel):
    user_name:str
    email:EmailStr
    college: Optional[str] = None
    role:str


class UserCreate(UserBase):
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class UserResponse(UserBase):
    id:UUID = Field(default_factory=uuid4)
    created_at:datetime = Field(default_factory=datetime.utcnow)
    updated_at:datetime = Field(default_factory=datetime.utcnow)