from fastapi import Depends

from modules.notifications.storage.notification_storage import NotificationStorage

from modules.audit.services.audit_service import AuditService
from modules.audit.depends.dependencies import get_audit_service
from api.deps.uow_dep import get_unit_of_work
from core.unit_of_work import UnitOfWork
from modules.notifications.service.notification_service import NotificationService


def get_notification_service(
    notification_storage: NotificationStorage = Depends(NotificationStorage),
    audit_service: AuditService = Depends(get_audit_service),
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> NotificationService:
    return NotificationService(
        notification_storage=notification_storage,
        audit_service=audit_service,
        uow=uow,
    )