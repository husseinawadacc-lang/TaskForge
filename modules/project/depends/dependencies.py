from fastapi import Depends
from modules.billing.service.billing_service import BillingService

# ==========================================================
# STORAGE
# ==========================================================
from modules.billing.depends.dependencies import get_billing_service
from modules.project.storage.project_storage import ProjectStorage
from modules.project.storage.project_member_storage import ProjectMemberStorage
from modules.user.storage.user_storage import UserStorage
from modules.project.depends.storage_dependes import (
    get_project_member_storage,get_project_storage
)
# ==========================================================
# CORE SERVICES
# ==========================================================

from core.unit_of_work import UnitOfWork
from modules.audit.services.audit_service import AuditService
# ==========================================================
# BUSINESS SERVICES
# ==========================================================

from modules.project.service.project_service import ProjectService
from modules.audit.depends.dependencies import get_audit_service
from api.deps.uow_dep import get_unit_of_work

# ==========================================================
# ProjectService 🔥 NEW
# ==========================================================

def get_project_service(
    project_storage: ProjectStorage = Depends(get_project_storage),
    member_storage: ProjectMemberStorage= Depends(get_project_member_storage),
    user_storage= UserStorage(),
    uow: UnitOfWork = Depends(get_unit_of_work),
    audit_service:AuditService = Depends(get_audit_service),
    billing_service: BillingService = Depends(get_billing_service),
) -> ProjectService:
    """
    ProjectService dependency.

    Handles:
    - Project creation
    - Ownership isolation
    - SaaS structure
    """

    return ProjectService(
        project_storage=project_storage,
        member_storage=member_storage,
        user_storage = user_storage,
        uow=uow,
        audit_service=audit_service,
        billing_service=billing_service,
    )
