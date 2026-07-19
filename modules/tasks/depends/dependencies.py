from fastapi import Depends

from modules.tasks.service.task_service import TaskService
from modules.tasks.storage.task_storage import TaskStorage
from modules.tasks.depends.storage_dependes import get_task_storage

# ==========================================================
# CORE SERVICES
# ==========================================================

from core.unit_of_work import UnitOfWork
from modules.audit.services.audit_service import AuditService
# ==========================================================
# BUSINESS SERVICES
# ==========================================================

from modules.tasks.service.task_service import TaskService
from modules.project.service.project_service import ProjectService
from modules.notifications.service.notification_service import NotificationService
from modules.audit.depends.dependencies import get_audit_service
from api.deps.uow_dep import get_unit_of_work
from modules.notifications.dependencies import  get_notification_service
from modules.project.depends.dependencies import get_project_service

# ==========================================================
# TaskService
# ==========================================================

def get_task_service(
    task_storage: TaskStorage = Depends(get_task_storage),
    uow: UnitOfWork = Depends(get_unit_of_work),
    project_service:ProjectService= Depends(get_project_service),
    audit_service:AuditService = Depends(get_audit_service),
    notification_service: NotificationService = Depends(get_notification_service),
) -> TaskService:

    return TaskService(
        task_storage=task_storage,
        uow=uow,
        project_service=project_service,
        audit_service=audit_service,
        notification_service=notification_service,
    )
