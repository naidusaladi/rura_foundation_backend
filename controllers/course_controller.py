from fastapi import HTTPException
from fastapi.responses import StreamingResponse
import httpx
from config.database import get_course_collection, get_module_collection, get_chapter_collection
from uuid import UUID

course_collection = get_course_collection()
module_collection = get_module_collection()
chapter_collection = get_chapter_collection()


async def get_courses():
    courses = list(course_collection.find({}, {"_id": 0}))
    return {"status": "success", "message": "Courses fetched", "body": courses}


async def get_course(course_id: UUID):
    course = course_collection.find_one({"course_id": str(course_id)}, {"_id": 0})
    if not course:
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Course not found", "body": None})
    # Ensure 'modules' field is always present and is a list
    if 'modules' not in course or not isinstance(course['modules'], list):
        course['modules'] = []
    return {"status": "success", "message": "Course fetched", "body": course}


async def get_course_image(course_id: UUID):
    course = course_collection.find_one({"course_id": str(course_id)}, {"_id": 0})
    if not course or "course_image_url" not in course:
        raise HTTPException(status_code=404, detail="Image not found")

    image_url = course["course_image_url"]
    if image_url.startswith("https://drive.google.com"):
        file_id = image_url.split("/").pop().split("?")[0]
        image_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(image_url, follow_redirects=True)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            # Stream the image content
            return StreamingResponse(response.iter_bytes(), media_type=response.headers.get("content-type"))
        
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"Failed to fetch image: {e}")
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while requesting the image: {e}")


# ---------- Module ----------
async def get_module(course_id: UUID, module_id: UUID):
    module = module_collection.find_one(
        {"course_id": str(course_id), "module_id": str(module_id)}, {"_id": 0}
    )
    if not module:
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Module not found", "body": None})
    return {"status": "success", "message": "Module fetched", "body": module}


# ---------- Chapter ----------
async def get_chapter(course_id: UUID, module_id: UUID, chapter_id: UUID):
    chapter = chapter_collection.find_one(
        {"course_id": str(course_id), "module_id": str(module_id), "chapter_id": str(chapter_id)}, {"_id": 0}
    )
    if not chapter:
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Chapter not found", "body": None})
    return {"status": "success", "message": "Chapter fetched", "body": chapter}
