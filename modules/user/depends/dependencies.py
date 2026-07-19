from fastapi import Depends
from modules.audit.storage.audit_storage import AuditStorage
from modules.audit.services.audit_service import AuditService

def get_audit_service(
    audit_storage = AuditStorage(),
) -> AuditService:
    """
    Provide AuditService instance.

    Responsibilities:
    - Log significant events (e.g., user logins, data changes)
    - Store audit logs in the database
    - Ensure immutability and integrity of logs
    """
    return AuditService(audit_storage=audit_storage)

