from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime
from uuid import UUID

# ---------- Course ----------
class CourseCreate(BaseModel):
    title: str
    description: str
    course_image_url: Optional[str] = None

class CourseResponse(BaseModel):
    course_id: UUID
    title: str
    description: Optional[str] = None
    course_image_url: Optional[HttpUrl] = None
    created_at: datetime
    updated_at: datetime

# ---------- Module ----------
class ModuleCreate(BaseModel):
    module_title: str
    module_description: Optional[str] = None
    module_number: int

class ModuleResponse(BaseModel):
    module_id: UUID
    course_id: UUID
    module_title: str
    module_description: Optional[str] = None
    module_number: int
    created_at: datetime
    updated_at: datetime

# ---------- Chapter ----------
class ChapterCreate(BaseModel):
    chapter_title: str
    chapter_content: str
    chapter_number: Optional[int] = None

class ChapterResponse(BaseModel):
    chapter_id: UUID
    course_id: UUID
    module_id: UUID
    chapter_title: str
    chapter_content: str
    chapter_number: int
    created_at: datetime
    updated_at: datetime
