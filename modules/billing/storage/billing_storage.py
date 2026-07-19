
from datetime import datetime,timezone
from sqlalchemy import select, func
from modules.billing.domain.models import Subscription
from db.models.subscription import SubscriptionORM
from core.exceptions import NotFoundError


class BillingStorage:

    def create_subscription(self, *, session, subscription: Subscription) -> Subscription:

        orm = SubscriptionORM(
            user_id=subscription.user_id,
            plan_id=subscription.plan_id,
            status=subscription.status,
            start_date=subscription.start_date,
            end_date=subscription.end_date,
        )

        session.add(orm)
        session.flush()

        return Subscription(
            id=orm.id,
            user_id=orm.user_id,
            plan_id=orm.plan_id,
            status=orm.status,
            start_date=orm.start_date,
            end_date=orm.end_date,
        )
    
    

    def get_active_subscription(self, *, session, user_id: int) -> Subscription:

        stmt = select(SubscriptionORM).where(
            SubscriptionORM.user_id == user_id,
                 )

        orm = session.execute(stmt).scalar_one_or_none()

        if not orm:
            raise NotFoundError("Active subscription not found")
        
        if orm.status == "canceled" or (orm.end_date and orm.end_date < datetime.utcnow()):
            raise NotFoundError("Active subscription not found")
        
        return Subscription(
            id=orm.id,
            user_id=orm.user_id,
            plan_id=orm.plan_id,
            status=orm.status,
            start_date=orm.start_date,
            end_date=orm.end_date,
        )
    
    def update_subscription(self, *, session, subscription: Subscription) -> Subscription:

        stmt = select(SubscriptionORM).where(
            SubscriptionORM.id == subscription.id
        )

        orm = session.execute(stmt).scalar_one_or_none()

        if not orm:
            raise NotFoundError("Subscription not found")

        orm.plan_id = subscription.plan_id
        orm.status = subscription.status
        orm.end_date = subscription.end_date

        session.flush()

        return subscription
    
    