
from modules.audit.domain.audit import AuditLog
from db.models.audit_log import AuditLogORM


class AuditStorage:

    def create_audit_log(self, *, session, log: AuditLog) -> AuditLog:

        orm = AuditLogORM(
            user_id=log.user_id,
            action=log.action,
            resource_type=log.resource_type,
            resource_id=log.resource_id,
            details=log.details,
        )

        session.add(orm)
        session.flush()

        return AuditLog(
            id=orm.id,
            user_id=orm.user_id,
            action=orm.action,
            resource_type=orm.resource_type,
            resource_id=orm.resource_id,
            details=orm.details,
            created_at=orm.created_at,
        ) 
    
    
   