from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime
from uuid import UUID

# ---------- Course ----------
class CourseResponse(BaseModel):
    course_id: UUID
    title: str
    description: Optional[str] = None
    course_image_url: Optional[HttpUrl] = None
    created_at: datetime
    updated_at: datetime

# ---------- Module ----------
class ModuleResponse(BaseModel):
    module_id: UUID
    course_id: UUID
    module_title: str
    module_description: Optional[str] = None
    module_number: int
    created_at: datetime
    updated_at: datetime

# ---------- Chapter ----------
class ChapterResponse(BaseModel):
    chapter_id: UUID
    course_id: UUID
    module_id: UUID
    chapter_content: str
    chapter_number: int
    created_at: datetime
    updated_at: datetime
