from fastapi import Depends
from storage.st_factory import get_storage
from services.audit_service import AuditService

def get_audit_service(
    storage = Depends(get_storage),
) -> AuditService:
    """
    Provide AuditService instance.

    Responsibilities:
    - Log significant events (e.g., user logins, data changes)
    - Store audit logs in the database
    - Ensure immutability and integrity of logs
    """
    return AuditService(storage=storage)

