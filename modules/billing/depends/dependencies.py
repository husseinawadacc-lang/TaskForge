from modules.billing.storage.billing_storage import BillingStorage
from core.unit_of_work import UnitOfWork
from modules.billing.service.billing_service import BillingService


def get_billing_service() -> BillingService:
    billing_storage = BillingStorage()
    uow = UnitOfWork()

    return BillingService(
        billing_storage=billing_storage,
        uow=uow,
    )