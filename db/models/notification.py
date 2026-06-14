from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from db.base import Base


class NotificationORM(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    # 🔥 أهم حاجة: مين المستقبل؟
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # نوع الإشعار (enum value)
    type = Column(String, nullable=False)

    # محتوى الإشعار
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)

    # حالة القراءة
    is_read = Column(Boolean, default=False,nullable=False)

    # optional references (ربط بـ domain تاني)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)

    # timestamp
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # # relationship
    # user = relationship("UserORM")

    __table_args__ = (
        Index("idx_notifications_user_id", "user_id"),
        Index("idx_notifications_user_unread","user_id", "is_read"),
    )