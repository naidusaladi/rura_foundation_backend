from fastapi import APIRouter, Depends
from uuid import UUID
from controllers import course_controller
from services.deps import get_current_user, get_admin_user
from schemas.course import CourseCreate, ModuleCreate, ChapterCreate

router = APIRouter(tags=["Courses"])


# ========== MOST SPECIFIC ROUTES FIRST ==========

# ---------- Chapter Routes ----------
@router.get("/{course_id}/modules/{module_id}/chapters/next-number")
async def get_next_chapter_number(course_id: UUID, module_id: UUID, admin_user: dict = Depends(get_admin_user)):
    next_number = await course_controller.get_next_chapter_number(course_id, module_id)
    return {"status": "success", "message": "Next chapter number retrieved", "body": {"next_chapter_number": next_number}}


@router.put("/{course_id}/modules/{module_id}/chapters/{chapter_id}")
async def update_chapter(course_id: UUID, module_id: UUID, chapter_id: UUID, chapter_data: ChapterCreate, admin_user: dict = Depends(get_admin_user)):
    return await course_controller.update_chapter(course_id, module_id, chapter_id, chapter_data)


@router.delete("/{course_id}/modules/{module_id}/chapters/{chapter_id}")
async def delete_chapter(course_id: UUID, module_id: UUID, chapter_id: UUID, admin_user: dict = Depends(get_admin_user)):
    print(f"DELETE chapter route called - course_id: {course_id}, module_id: {module_id}, chapter_id: {chapter_id}")
    return await course_controller.delete_chapter(course_id, module_id, chapter_id)


@router.get("/{course_id}/modules/{module_id}/chapters/{chapter_id}")
async def get_chapter(course_id: UUID, module_id: UUID, chapter_id: UUID, user: dict = Depends(get_current_user)):
    return await course_controller.get_chapter(course_id, module_id, chapter_id)


@router.post("/{course_id}/modules/{module_id}/chapters")
async def create_chapter(course_id: UUID, module_id: UUID, chapter_data: ChapterCreate, admin_user: dict = Depends(get_admin_user)):
    return await course_controller.create_chapter(course_id, module_id, chapter_data)


@router.get("/{course_id}/modules/{module_id}/chapters")
async def get_module_chapters(course_id: UUID, module_id: UUID):
    return await course_controller.get_module_chapter(course_id, module_id)


# ---------- Module Routes ----------
@router.delete("/{course_id}/modules/{module_id}")
async def delete_module(course_id: UUID, module_id: UUID, admin_user: dict = Depends(get_admin_user)):
    print(f"DELETE module route called - course_id: {course_id}, module_id: {module_id}")
    return await course_controller.delete_module(course_id, module_id)


@router.get("/{course_id}/modules/{module_id}")
async def get_module(course_id: UUID, module_id: UUID, user: dict = Depends(get_current_user)):
    return await course_controller.get_module(course_id, module_id)


@router.post("/{course_id}/modules")
async def create_module(course_id: UUID, module_data: ModuleCreate, admin_user: dict = Depends(get_admin_user)):
    return await course_controller.create_module(course_id, module_data)


@router.get("/{course_id}/modules")
async def get_course_modules(course_id: UUID, user: dict = Depends(get_current_user)):
    return await course_controller.get_course_modules(course_id)


# ---------- Course Routes ----------
@router.delete("/{course_id}")
async def delete_course(course_id: UUID, admin_user: dict = Depends(get_admin_user)):
    return await course_controller.delete_course(course_id)


@router.get("/{course_id}/image")
async def get_course_image(course_id: UUID):
    return await course_controller.get_course_image(course_id)


@router.get("/{course_id}")
async def get_course(course_id: UUID, user: dict = Depends(get_current_user)):
    return await course_controller.get_course(course_id)


@router.post("/")
async def create_course(course_data: CourseCreate, admin_user: dict = Depends(get_admin_user)):
    return await course_controller.create_course(course_data)


@router.get("/", dependencies=[Depends(get_current_user)])
async def get_courses():
    return await course_controller.get_courses()
