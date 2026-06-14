from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime, timezone

from db.base import Base


class SubscriptionORM(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)

    status = Column(String, nullable=False)  # active, canceled, past_due

    start_date = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    end_date = Column(DateTime, nullable=True)