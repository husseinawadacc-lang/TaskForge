from fastapi import APIRouter
from api.v1.routes import auth,health
from modules.ai.api import ai
from modules.tasks.api import tasks
from modules.project.api import project

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(tasks.router)
api_router.include_router(project.router)
api_router.include_router(health.router)
api_router.include_router(ai.router)
