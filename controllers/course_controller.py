from fastapi import HTTPException
from fastapi.responses import StreamingResponse
import httpx
from config.database import get_course_collection, get_module_collection, get_chapter_collection
from uuid import UUID, uuid4
from datetime import datetime
from schemas.course import CourseCreate, ModuleCreate, ChapterCreate

course_collection = get_course_collection()
module_collection = get_module_collection()
chapter_collection = get_chapter_collection()


def new_course(title: str, description: str, course_image_url: str = None):
    course_id = str(uuid4())
    now = datetime.utcnow()
    return {
        "course_id": course_id,
        "title": title,
        "description": description,
        "course_image_url": course_image_url,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat()
    }


def new_module(course_id: str, module_title: str, module_description: str = None, module_number: int = 1):
    module_id = str(uuid4())
    now = datetime.utcnow()
    return {
        "module_id": module_id,
        "course_id": course_id,
        "module_title": module_title,
        "module_description": module_description,
        "module_number": module_number,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat()
    }


def new_chapter(course_id: str, module_id: str, chapter_title: str, chapter_content: str, chapter_number: int = 1):
    chapter_id = str(uuid4())
    now = datetime.utcnow()
    return {
        "chapter_id": chapter_id,
        "course_id": course_id,
        "module_id": module_id,
        "chapter_title": chapter_title,
        "chapter_content": chapter_content,
        "chapter_number": chapter_number,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat()
    }


async def create_course(course_data: CourseCreate):
    try:
        course = new_course(
            title=course_data.title,
            description=course_data.description,
            course_image_url=course_data.course_image_url
        )
        
        # Create a copy for insertion to avoid modifying the original
        course_to_insert = course.copy()
        result = course_collection.insert_one(course_to_insert)
        
        if result.inserted_id:
            # Return the original course object without _id
            return {"status": "success", "message": "Course created successfully", "body": course}
        else:
            raise HTTPException(status_code=500, detail={"status": "error", "message": "Failed to create course", "body": None})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"status": "error", "message": f"Error creating course: {str(e)}", "body": None})


async def delete_course(course_id: UUID):
    try:
        # Check if course exists
        course = course_collection.find_one({"course_id": str(course_id)}, {"_id": 0})
        if not course:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Course not found", "body": None})
        
        # Delete the course
        result = course_collection.delete_one({"course_id": str(course_id)})
        
        if result.deleted_count > 0:
            # Also delete related modules and chapters
            module_collection.delete_many({"course_id": str(course_id)})
            chapter_collection.delete_many({"course_id": str(course_id)})
            
            return {"status": "success", "message": "Course deleted successfully", "body": {"course_id": str(course_id)}}
        else:
            raise HTTPException(status_code=500, detail={"status": "error", "message": "Failed to delete course", "body": None})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"status": "error", "message": f"Error deleting course: {str(e)}", "body": None})


async def create_module(course_id: UUID, module_data: ModuleCreate):
    try:
        print(f"Creating module for course_id: {course_id}")
        print(f"Module data: {module_data}")
        
        # Check if course exists
        course = course_collection.find_one({"course_id": str(course_id)}, {"_id": 0})
        print(f"Found course: {course}")
        
        if not course:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Course not found", "body": None})
        
        # Create the module
        module = new_module(
            course_id=str(course_id),
            module_title=module_data.module_title,
            module_description=module_data.module_description,
            module_number=module_data.module_number
        )
        
        print(f"Created module object: {module}")
        
        # Create a copy for insertion to avoid modifying the original
        module_to_insert = module.copy()
        result = module_collection.insert_one(module_to_insert)
        
        print(f"Insert result: {result.inserted_id}")
        
        if result.inserted_id:
            return {"status": "success", "message": "Module created successfully", "body": module}
        else:
            raise HTTPException(status_code=500, detail={"status": "error", "message": "Failed to create module", "body": None})
    except HTTPException:
        raise
    except Exception as e:
        print(f"Exception in create_module: {str(e)}")
        raise HTTPException(status_code=500, detail={"status": "error", "message": f"Error creating module: {str(e)}", "body": None})


async def get_next_chapter_number(course_id: UUID, module_id: UUID):
    try:
        # Get the highest chapter number for this module
        chapters = list(chapter_collection.find(
            {"course_id": str(course_id), "module_id": str(module_id)}, 
            {"chapter_number": 1, "_id": 0}
        ).sort("chapter_number", -1).limit(1))
        
        if chapters:
            return chapters[0]["chapter_number"] + 1
        else:
            return 1
    except Exception as e:
        print(f"Error getting next chapter number: {str(e)}")
        return 1


async def create_chapter(course_id: UUID, module_id: UUID, chapter_data: ChapterCreate):
    try:
        print(f"Creating chapter for course_id: {course_id}, module_id: {module_id}")
        print(f"Chapter data: {chapter_data}")
        
        # Check if course exists
        course = course_collection.find_one({"course_id": str(course_id)}, {"_id": 0})
        if not course:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Course not found", "body": None})
        
        # Check if module exists
        module = module_collection.find_one({"course_id": str(course_id), "module_id": str(module_id)}, {"_id": 0})
        if not module:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Module not found", "body": None})
        
        # Auto-generate chapter number
        next_chapter_number = await get_next_chapter_number(course_id, module_id)
        
        # Create the chapter
        chapter = new_chapter(
            course_id=str(course_id),
            module_id=str(module_id),
            chapter_title=chapter_data.chapter_title,
            chapter_content=chapter_data.chapter_content,
            chapter_number=next_chapter_number
        )
        
        print(f"Created chapter object: {chapter}")
        
        # Create a copy for insertion to avoid modifying the original
        chapter_to_insert = chapter.copy()
        result = chapter_collection.insert_one(chapter_to_insert)
        
        print(f"Insert result: {result.inserted_id}")
        
        if result.inserted_id:
            return {"status": "success", "message": "Chapter created successfully", "body": chapter}
        else:
            raise HTTPException(status_code=500, detail={"status": "error", "message": "Failed to create chapter", "body": None})
    except HTTPException:
        raise
    except Exception as e:
        print(f"Exception in create_chapter: {str(e)}")
        raise HTTPException(status_code=500, detail={"status": "error", "message": f"Error creating chapter: {str(e)}", "body": None})


async def delete_module(course_id: UUID, module_id: UUID):
    try:
        # Check if module exists
        module = module_collection.find_one({"course_id": str(course_id), "module_id": str(module_id)}, {"_id": 0})
        if not module:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Module not found", "body": None})
        
        # Delete the module
        result = module_collection.delete_one({"course_id": str(course_id), "module_id": str(module_id)})
        
        if result.deleted_count > 0:
            # Also delete all chapters in this module
            chapter_collection.delete_many({"course_id": str(course_id), "module_id": str(module_id)})
            
            return {"status": "success", "message": "Module deleted successfully", "body": {"module_id": str(module_id)}}
        else:
            raise HTTPException(status_code=500, detail={"status": "error", "message": "Failed to delete module", "body": None})
    except HTTPException:
        raise
    except Exception as e:
        print(f"Exception in delete_module: {str(e)}")
        raise HTTPException(status_code=500, detail={"status": "error", "message": f"Error deleting module: {str(e)}", "body": None})


async def update_chapter(course_id: UUID, module_id: UUID, chapter_id: UUID, chapter_data: ChapterCreate):
    try:
        print(f"Updating chapter - course_id: {course_id}, module_id: {module_id}, chapter_id: {chapter_id}")
        
        # Check if chapter exists
        chapter = chapter_collection.find_one({
            "course_id": str(course_id), 
            "module_id": str(module_id), 
            "chapter_id": str(chapter_id)
        }, {"_id": 0})
        
        if not chapter:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Chapter not found", "body": None})
        
        # Update the chapter
        update_data = {
            "chapter_title": chapter_data.chapter_title,
            "chapter_content": chapter_data.chapter_content,
            "chapter_number": chapter_data.chapter_number,
            "updated_at": datetime.utcnow().isoformat()
        }
        
        result = chapter_collection.update_one(
            {"course_id": str(course_id), "module_id": str(module_id), "chapter_id": str(chapter_id)},
            {"$set": update_data}
        )
        
        if result.modified_count > 0:
            # Get the updated chapter
            updated_chapter = chapter_collection.find_one({
                "course_id": str(course_id), 
                "module_id": str(module_id), 
                "chapter_id": str(chapter_id)
            }, {"_id": 0})
            
            return {"status": "success", "message": "Chapter updated successfully", "body": updated_chapter}
        else:
            raise HTTPException(status_code=500, detail={"status": "error", "message": "Failed to update chapter", "body": None})
    except HTTPException:
        raise
    except Exception as e:
        print(f"Exception in update_chapter: {str(e)}")
        raise HTTPException(status_code=500, detail={"status": "error", "message": f"Error updating chapter: {str(e)}", "body": None})


async def delete_chapter(course_id: UUID, module_id: UUID, chapter_id: UUID):
    try:
        print(f"Deleting chapter - course_id: {course_id}, module_id: {module_id}, chapter_id: {chapter_id}")
        
        # Check if chapter exists
        chapter = chapter_collection.find_one({
            "course_id": str(course_id), 
            "module_id": str(module_id), 
            "chapter_id": str(chapter_id)
        }, {"_id": 0})
        
        print(f"Found chapter: {chapter}")
        
        if not chapter:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Chapter not found", "body": None})
        
        # Delete the chapter
        result = chapter_collection.delete_one({
            "course_id": str(course_id), 
            "module_id": str(module_id), 
            "chapter_id": str(chapter_id)
        })
        
        print(f"Delete result: {result.deleted_count}")
        
        if result.deleted_count > 0:
            return {"status": "success", "message": "Chapter deleted successfully", "body": {"chapter_id": str(chapter_id)}}
        else:
            raise HTTPException(status_code=500, detail={"status": "error", "message": "Failed to delete chapter", "body": None})
    except HTTPException:
        raise
    except Exception as e:
        print(f"Exception in delete_chapter: {str(e)}")
        raise HTTPException(status_code=500, detail={"status": "error", "message": f"Error deleting chapter: {str(e)}", "body": None})


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


# New function to get all modules for a course with their chapters
async def get_course_modules(course_id: UUID):
    modules = list(module_collection.find({"course_id": str(course_id)}, {"_id": 0}).sort("module_number", 1))
    
    # Don't raise an error if no modules found, just return empty list
    if not modules:
        return {"status": "success", "message": "No modules found for this course", "body": []}
    
    # Add chapters to each module, sorted by chapter_number
    for module in modules:
        chapters = list(chapter_collection.find({"course_id": str(course_id), "module_id": module["module_id"]}, {"_id": 0}).sort("chapter_number", 1))
        module["chapters"] = chapters
    
    return {"status": "success", "message": "Modules with chapters fetched", "body": modules}
   
async def get_module_chapter(course_id: UUID, module_id: UUID):
    chapters = list(chapter_collection.find({"course_id": str(course_id), "module_id": str(module_id)}, {"_id": 0}))
    if not chapters:
        raise HTTPException(status_code=404, detail={"status": "error", "message": "No chapters found for this module", "body": None})
    return {"status": "success", "message": "Chapters fetched", "body": chapters}

# ---------- Module ----------
async def get_module(course_id: UUID, module_id: UUID):
    module = module_collection.find_one(
        {"course_id": str(course_id), "module_id": str(module_id)}, {"_id": 0}
    )
    if not module:
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Module not found", "body": None})
    
    # Add chapters to the module, sorted by chapter_number
    chapters = list(chapter_collection.find({"course_id": str(course_id), "module_id": str(module_id)}, {"_id": 0}).sort("chapter_number", 1))
    module["chapters"] = chapters
    
    return {"status": "success", "message": "Module with chapters fetched", "body": module}

# ---------- Chapter ----------
async def get_chapter(course_id: UUID, module_id: UUID, chapter_id: UUID):
    chapter = chapter_collection.find_one(
        {"course_id": str(course_id), "module_id": str(module_id), "chapter_id": str(chapter_id)}, {"_id": 0}
    )
    if not chapter:
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Chapter not found", "body": None})
    return {"status": "success", "message": "Chapter fetched", "body": chapter}
