from fastapi import APIRouter, Depends

from modules.auth.depends.auth_dependencies import get_current_user
from modules.billing.depends.dependencies import get_billing_service
from modules.billing.schemas.billing import CheckoutResponse
from modules.billing.service.billing_service import BillingService
from core.unit_of_work import UnitOfWork
from api.deps.uow_dep import get_unit_of_work


router = APIRouter(prefix="/billing", tags=["Billing"])
# =====================================================
# UPGRADE
# =====================================================
@router.post("/upgrade")
def upgrade_plan(
    plan_id: int,
    current_user=Depends(get_current_user),
    billing_service: BillingService = Depends(get_billing_service),
    uow: UnitOfWork = Depends(get_unit_of_work),
):
    with uow as session:
        return billing_service.upgrade_plan(
            session=session,
            user_id=current_user.id,
            new_plan_id=plan_id,
        )


# =====================================================
# DOWNGRADE
# =====================================================
@router.post("/downgrade")
def downgrade_plan(
    current_user=Depends(get_current_user),
    billing_service: BillingService = Depends(get_billing_service),
    uow: UnitOfWork = Depends(get_unit_of_work),
):
    with uow as session:
        return billing_service.downgrade_plan(
            session=session,
            user_id=current_user.id,
        )


# =====================================================
# CANCEL
# =====================================================
@router.post("/cancel")
def cancel_subscription(
    current_user=Depends(get_current_user),
    billing_service: BillingService = Depends(get_billing_service),
    uow: UnitOfWork = Depends(get_unit_of_work),
):
    with uow as session:
        return billing_service.cancel_subscription(
            session=session,
            user_id=current_user.id,
        )


# =====================================================
# CHECKOUT
# =====================================================
@router.post("/checkout", response_model=CheckoutResponse)
def create_checkout(
    plan_id: int,
    current_user=Depends(get_current_user),
    billing_service: BillingService = Depends(get_billing_service),
):
    url = billing_service.create_checkout_session(
        user_id=current_user.id,
        plan_id=plan_id,
    )

    return CheckoutResponse(checkout_url=url)

@router.get("")
def get_billing_info(
    current_user=Depends(get_current_user),
    billing_service: BillingService = Depends(get_billing_service),
    uow: UnitOfWork = Depends(get_unit_of_work),
):
    with uow as session:
        return billing_service.get_subscription(
            session=session,
            user_id=current_user.id,
        )