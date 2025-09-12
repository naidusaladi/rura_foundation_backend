from fastapi import APIRouter, Depends
from uuid import UUID
from controllers import course_controller
from services.deps import get_current_user

router = APIRouter(tags=["Courses"])


# ---------- Courses ----------
@router.get("/", dependencies=[Depends(get_current_user)])
# @router.get("/")
async def get_courses():
    return await course_controller.get_courses()


@router.get("/{course_id}")
async def get_course(course_id: UUID, user: dict = Depends(get_current_user)):
    return await course_controller.get_course(course_id)


@router.get("/{course_id}/image")
async def get_course_image(course_id: UUID):
    return await course_controller.get_course_image(course_id)


# ---------- Modules ----------
@router.get("/{course_id}/modules/{module_id}")
async def get_module(course_id: UUID, module_id: UUID, user: dict = Depends(get_current_user)):
    return await course_controller.get_module(course_id, module_id)


# ---------- Chapters ----------
@router.get("/{course_id}/modules/{module_id}/chapters/{chapter_id}")
async def get_chapter(course_id: UUID, module_id: UUID, chapter_id: UUID, user: dict = Depends(get_current_user)):
    return await course_controller.get_chapter(course_id, module_id, chapter_id)
