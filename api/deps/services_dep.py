# ==========================================================
# Services Dependency Injection
# ==========================================================
"""
This module wires all services using FastAPI Depends.

Design Principles:
------------------
✔ Each request gets fresh service instances
✔ Dependencies are injected (NOT created manually in endpoints)
✔ Storage is abstracted (SQLAlchemy / Memory interchangeable)
✔ UnitOfWork manages transactions (NOT API layer)

Flow:
API → Depends → Service → Storage → DB
"""

from fastapi import Depends
from modules.billing.service.billing_service import BillingService

# ==========================================================
# STORAGE
# ==========================================================

from modules.billing.depends.dependencies import get_billing_service
from modules.notifications.dependencies import get_notification_service
from storage.base_st import BaseStorage
from storage.st_factory import get_storage

# ==========================================================
# CORE SERVICES
# ==========================================================

from services.unit_of_work import UnitOfWork
from services.password_policy_service import PasswordPolicyService
from services.audit_service import AuditService
# ==========================================================
# BUSINESS SERVICES
# ==========================================================

from services.token_services import TokenService
from services.auth_service import AuthService
from services.password_reset_services import PasswordResetService
from modules.notifications.service.notification_service import NotificationService
from api.deps.audit_dep import get_audit_service
from api.deps.uow_dep import get_unit_of_work

# ==========================================================
# Password Policy
# ==========================================================

def get_password_policy_service() -> PasswordPolicyService:
    """
    Stateless service.

    Safe to instantiate per request.
    No DB access required.
    """
    return PasswordPolicyService()





# ==========================================================
# TokenService
# ==========================================================

def get_token_service(
    storage: BaseStorage = Depends(get_storage),
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> TokenService:
    """
    TokenService dependency.

    Handles:
    - JWT creation
    - Refresh tokens
    - Token lifecycle
    """

    return TokenService(
        storage=storage,
        uow=uow,
    )


# ==========================================================
# AuthService
# ==========================================================

def get_auth_service(
    storage: BaseStorage = Depends(get_storage),
    policy: PasswordPolicyService = Depends(get_password_policy_service),
    uow: UnitOfWork = Depends(get_unit_of_work),
    token_service: TokenService = Depends(get_token_service),
    billing_service: BillingService = Depends(get_billing_service),
) -> AuthService:
    """
    AuthService dependency.

    Handles:
    - Login / Register
    - Password validation
    - Token issuing
    """

    return AuthService(
        storage=storage,
        password_policy=policy,
        uow=uow,
        token_service=token_service,
        billing_service=billing_service,
    )


# ==========================================================
# Password Reset Service
# ==========================================================

def get_password_reset_service(
    storage: BaseStorage = Depends(get_storage),
    policy: PasswordPolicyService = Depends(get_password_policy_service),
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> PasswordResetService:
    """
    Password reset flow.

    Handles:
    - Generate reset token
    - Validate token
    - Update password securely
    """

    return PasswordResetService(
        storage=storage,
        password_policy=policy,
        uow=uow,
    )
