from datetime import datetime, timedelta
from modules.billing.domain.models import Subscription
from modules.billing.domain.plans import get_plan
from datetime import datetime, timedelta
from core.config import get_settings
import stripe
from modules.billing.storage.billing_storage import BillingStorage
from core.unit_of_work import UnitOfWork

settings = get_settings()

stripe.api_key = settings.STRIPE_SECRET_KEY

class BillingService:

    def __init__(self, billing_storage: BillingStorage, uow: UnitOfWork):
        self.billing_storage = billing_storage
        self.uow = uow

    # ==========================
    # CREATE FREE SUBSCRIPTION
    # ==========================
    def create_free_subscription(self,*,session, user_id: int):


        sub = Subscription(
            id=None,
            user_id=user_id,
            plan_id=1,
            status="active",
            start_date=datetime.utcnow(),
            end_date=None,
        )

        return self.billing_storage.create_subscription(
            session=session,
            subscription=sub
        )

    # ==========================
    # CHECK LIMIT
    # ==========================
    def can_create_project(self, *,session, user_id: int, current_projects: int) -> bool:

    

        sub = self.billing_storage.get_active_subscription(
            session=session,
            user_id=user_id
        )

        plan = get_plan(sub.plan_id)

        if plan.max_projects is None:
            return True

        return current_projects < plan.max_projects
    
    # ==========================
    # UPGRADE SUBSCRIPTION
    # ==========================
    def upgrade_plan(self, *,session, user_id: int, new_plan_id: int):

        sub = self.billing_storage.get_active_subscription(
            session=session,
            user_id=user_id
        )

        if sub is None:
            raise Exception("No active subscription found")

        sub.plan_id = new_plan_id
        sub.start_date = datetime.utcnow()
        sub.end_date = None

        return self.billing_storage.update_subscription(
            session=session,
            subscription=sub
        )
    
    # ==========================
    # DOWNGRADE SUBSCRIPTION    
    # ==========================
    def downgrade_plan(
        self,
        *,
        session,
        user_id: int,
        new_plan_id: int = 1  # FREE
    ):

        # 1️⃣ get subscription
        sub = self.billing_storage.get_active_subscription(
            session=session,
            user_id=user_id
        )

        # 2️⃣ update plan
        sub.plan_id = new_plan_id

        # 3️⃣ persist
        updated = self.billing_storage.update_subscription(
            session=session,
            subscription=sub
        )

        return updated
    
    # ==========================
    # CANCEL SUBSCRIPTION
    # ==========================
    def cancel_subscription(
            self,
            *,
            session,
            user_id: int
        ):

            sub = self.billing_storage.get_active_subscription(
                session=session,
                user_id=user_id
            )

            # 🔥 mark as canceled
            sub.status = "canceled"

            # 🔥 set end date (مثلاً بعد 30 يوم)
            sub.end_date = datetime.utcnow() + timedelta(days=30)

            updated = self.billing_storage.update_subscription(
                session=session,
                subscription=sub
            )

            return updated


    def create_checkout_session(
        self,
        *,
        user_id: int,
        plan_id: int
    ):

        # 🔥 هنا نحدد السعر
        plan = get_plan(plan_id)
        print("plan", plan)
        print("plan_id", plan_id)
        if plan_id is None:
            raise ValueError("Invalid plan")

        price = int(plan.price)
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "Pro Plan",
                    },
                    "unit_amount": price,
                },
                "quantity": 1,
            }],
            success_url="http://localhost:3000/success",
            cancel_url="http://localhost:3000/cancel",

            # 🔥 مهم جدًا
            metadata={
                "user_id": str(user_id),
                "plan_id": str(plan_id),
            }
        )

        return session.url

    def get_subscription(self,*,session,user_id: int):
        return self.billing_storage.get_active_subscription(
            session=session,
            user_id=user_id
        )