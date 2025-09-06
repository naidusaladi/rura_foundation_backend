from fastapi import FastAPI
from routes import user_routes

app = FastAPI()

# Routes
app.include_router(user_routes.router)
