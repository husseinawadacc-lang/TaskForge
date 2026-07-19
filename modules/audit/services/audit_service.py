from modules.audit.domain.audit import AuditLog
from datetime import datetime, timezone
from modules.audit.storage.audit_storage import AuditStorage


class AuditService:

    def __init__(self, audit_storage:AuditStorage):
        self.audit_storage = audit_storage

    def log(
        self,
        *,
        session,
        user_id: int,
        action: str,
        resource_type: str,
        resource_id: int | None = None,
        details: dict | None = None,
    ):
        log = AuditLog(
            id=None,
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            created_at=datetime.now(timezone.utc),
        )

        self.audit_storage.create_audit_log(
            session=session,
            log=log,
        )