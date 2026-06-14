from modules.notifications.domain.models import Notification
from modules.notifications.domain.enums import NotificationType
from modules.notifications.storage.notification_storage import NotificationStorage
from services.audit_service import AuditService
from services.unit_of_work import UnitOfWork


class NotificationService:

    def __init__(self, notification_storage: NotificationStorage, audit_service: AuditService, uow: UnitOfWork):
        self.notifaction_storage = notification_storage
        self.audit_service = audit_service
        self.uow = uow

    # 🔥 Core method
    def create_notification(
        self,
        user_id: int,
        type: NotificationType,
        title: str,
        message: str,
        task_id: int | None = None,
        project_id: int | None = None,
        actor_id: int | None = None,
    ):

        with self.uow as session:

            notification = Notification(
                id=None,
                user_id=user_id,
                type=type.value,
                title=title,
                message=message,
                task_id=task_id,
                project_id=project_id,
            )

            notification = self.notifaction_storage.create_notification(
                session=session,
                notification=notification
            )

            # 🔥 Audit داخل نفس transaction
            if actor_id:
                self.audit_service.log(
                    
                    session=session,
                    user_id=actor_id,
                    action="notification_created",
                    resource_type="notification",
                    resource_id=notification.id,
                    details={
                        "type": type.value,
                        "user_id": user_id,
                    }
                )

            return notification


    # 🎯 Use case: Task Assigned
    def notify_task_assigned(self, task, assigned_user_id, actor_id):

        
            return self.create_notification(
                user_id=assigned_user_id,
                type=NotificationType.TASK_ASSIGNED,
                title=NotificationType.TASK_ASSIGNED.label(),
                message=f"You were assigned to: {task.title}",
                task_id=task.id,
                project_id=task.project_id,
                actor_id=actor_id,
            )
    
    def get_user_notifications(self, user_id: int):
        
        with self.uow as session:
            return self.notifaction_storage.get_notifications_by_user(
                user_id=user_id, session=session  )
    
    def mark_as_read(self, notification_id: int, user_id: int) -> bool:

        with self.uow as session:
            return self.notifaction_storage.mark_notification_as_read(
                notification_id=notification_id, user_id=user_id, session=session)
    
    def get_unread_count(self, user_id: int) -> int:
        with self.uow as session:
            return self.notifaction_storage.get_unread_notifications_count(
            user_id=user_id, session=session )