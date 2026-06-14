from typing import List

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from modules.notifications.domain.models import Notification

from db.models.notification import NotificationORM

from utils.exceptions import NotFoundError


class NotificationStorage:

    def map_notification(self, orm: NotificationORM) -> Notification:
        return Notification(
            id=orm.id,
            user_id=orm.user_id,
            type=orm.type,
            title=orm.title,
            message=orm.message,
            is_read=orm.is_read,
            created_at=orm.created_at,
            task_id=orm.task_id,
            project_id=orm.project_id,
        )
    
    def create_notification(
    self,
    *,
    session: Session,
    notification: Notification
) -> Notification:

        orm = NotificationORM(
            user_id=notification.user_id,
            type=notification.type,
            title=notification.title,
            message=notification.message,
            task_id=notification.task_id,
            project_id=notification.project_id,
        )

        session.add(orm)
        session.flush()

        return self.map_notification(orm)
    
    def get_notifications_by_user(
    self,
    *,
    session: Session,
    user_id: int
) -> List[Notification]:

        stmt = select(NotificationORM).where(
            NotificationORM.user_id == user_id
        ).order_by(NotificationORM.created_at.desc())

        notifications = session.execute(stmt).scalars().all()

        return [self.map_notification(n) for n in notifications]
    
    def mark_notification_as_read(
    self,
    *,
    session: Session,
    notification_id: int,
    user_id: int
) -> bool:

        stmt = select(NotificationORM).where(
            NotificationORM.id == notification_id,
            NotificationORM.user_id == user_id
        )

        orm = session.execute(stmt).scalar_one_or_none()

        if not orm:
            raise NotFoundError("Notification not found")

        if orm.is_read:
            return False

        orm.is_read = True
        session.flush()

        return True
    
    def get_unread_notifications_count(
    self,
    *,
    session: Session,
    user_id: int
) -> int:

        stmt = select(func.count()).where(
            NotificationORM.user_id == user_id,
            NotificationORM.is_read == False
        )

        return session.execute(stmt).scalar_one()
