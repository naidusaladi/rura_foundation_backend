from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routes import user_routes, course_routes  # import your routes

app = FastAPI()

# ✅ Mount static files
# app.mount("/images", StaticFiles(directory="./rura_images"), name="images")

# ✅ Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],   
)

# ✅ Include routes
app.include_router(user_routes.router, tags=["Users"])
app.include_router(course_routes.router, prefix="/courses", tags=["Courses"])
