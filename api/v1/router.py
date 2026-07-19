from fastapi import APIRouter
from modules.auth.api import auth
from modules.ai.api import ai
from modules.tasks.api import tasks
from modules.project.api import project
from modules.billing.api import billing
from modules.notifications.api import notification
from modules.billing.api import webhook
api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(tasks.router)
api_router.include_router(project.router)
api_router.include_router(billing.router)
api_router.include_router(notification.router)
api_router.include_router(webhook.router)

api_router.include_router(ai.router)
