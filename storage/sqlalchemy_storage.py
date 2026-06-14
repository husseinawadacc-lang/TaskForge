"""
SQLAlchemyStorage
=================

This storage implementation uses SQLAlchemy ORM.

Important architectural rules:

1) Storage NEVER controls transactions
   - No commit
   - No rollback

2) Transaction lifecycle is handled by UnitOfWork.

3) Storage only performs:
   - queries
   - inserts
   - updates
   - deletes

4) flush() is used instead of commit() to obtain generated IDs.
"""

from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from storage.base_st import (
    BaseStorage,
    PasswordResetTokenRecord,
    RefreshTokenRecord)
from domain.user import User
from domain.audit_log import AuditLog
from db.models.user import UserORM
from db.models.password_reset import PasswordResetTokenORM
from db.models.refresh_token import RefreshTokenORM
from db.models.audit_log import AuditLogORM
from sqlalchemy.exc import IntegrityError
from utils.exceptions import NotFoundError,ConflictError


class SQLAlchemyStorage(BaseStorage):

    # ==========================================================
    # USER OPERATIONS
    # ==========================================================

    def create_user(self, *, session:Session, user: User) -> User:
        """
        Persist new user.
        """

        orm_user = UserORM(
            email=user.email,
            password_hash=user.password_hash,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
        )

        session.add(orm_user)

        # flush sends SQL but does NOT commit
        try: 
            session.flush()
        except IntegrityError as e:
            raise ConflictError ("resource already exists") from e
        
        return User(
                    id=orm_user.id,
                    email=orm_user.email,
                    password_hash=orm_user.password_hash,
                    role=orm_user.role,
                    is_active=orm_user.is_active,
                    created_at=orm_user.created_at,
                )

    # ----------------------------------------------------------

    def update_user(self, *, session:Session, user: User) -> User:
        """
        Update existing user.
        """

        stmt = select(UserORM).where(UserORM.id == user.id)

        orm_user = session.execute(stmt).scalar_one_or_none()

        if not orm_user:
            raise NotFoundError("User not found")

        orm_user.email = user.email
        orm_user.role = user.role
        orm_user.is_active = user.is_active

        session.flush()

        return user

    # ----------------------------------------------------------

    def get_user_by_id(self, *, session:Session, user_id: int) -> User:

        stmt = select(UserORM).where(UserORM.id == user_id)

        orm_user = session.execute(stmt).scalar_one_or_none()

        if not orm_user:
            raise NotFoundError("User not found")

        return User(
            id=orm_user.id,
            email=orm_user.email,
            password_hash=orm_user.password_hash,
            role=orm_user.role,
            is_active=orm_user.is_active,
            created_at=orm_user.created_at,
        )

    # ----------------------------------------------------------

    def get_user_by_email(self, *, session:Session, email: str) -> User:

        stmt = select(UserORM).where(UserORM.email == email)

        orm_user = session.execute(stmt).scalar_one_or_none()

        if not orm_user:
            raise NotFoundError("User not found")

        return User(
            id=orm_user.id,
            email=orm_user.email,
            password_hash=orm_user.password_hash,
            role=orm_user.role,
            is_active=orm_user.is_active,
            created_at=orm_user.created_at,
        )

    # ----------------------------------------------------------

    def update_user_password(
        self,
        *,
        session:Session,
        user_id: int,
        password_hash: str
    ) -> None:

        stmt = select(UserORM).where(UserORM.id == user_id)

        orm_user = session.execute(stmt).scalar_one_or_none()

        if not orm_user:
            raise NotFoundError("User not found")

        orm_user.password_hash = password_hash

        session.flush()


    # ------------------------------------------------------
    # def map_task_with_subtasks(self,orm: TaskORM) -> Task:
    #     task = self.map_task(orm)

    #     task.subtasks = [
    #         self.map_task(sub) for sub in orm.subtasks
    #     ]

    #     return task

    # ==========================================================
    # PASSWORD RESET TOKENS
    # ==========================================================

    def create_password_reset_token(
        self,
        *,
        session:Session,
        user_id: int,
        token_hash: str,
        expires_at: datetime
    ) -> int:

        orm_token = PasswordResetTokenORM(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            used=False,
        )

        session.add(orm_token)

        session.flush()

        return orm_token.id

    # ----------------------------------------------------------

    def get_password_reset_token(
        self,
        *,
        session:Session,
        token_hash: str
    ) -> PasswordResetTokenRecord:

        stmt = select(PasswordResetTokenORM).where(
            PasswordResetTokenORM.token_hash == token_hash
        )

        orm_token = session.execute(stmt).scalar_one_or_none()

        if not orm_token:
            raise NotFoundError("Reset token not found")

        return PasswordResetTokenRecord(
            id=orm_token.id,
            user_id=orm_token.user_id,
            token_hash=orm_token.token_hash,
            expires_at=orm_token.expires_at,
            used=orm_token.used,
        )

    # ----------------------------------------------------------

    def mark_password_reset_token_used(
        self,
        *,
        session:Session,
        token_id: int
    ) -> None:

        stmt = select(PasswordResetTokenORM).where(
            PasswordResetTokenORM.id == token_id
        )

        orm_token = session.execute(stmt).scalar_one_or_none()

        if not orm_token:
            raise NotFoundError("Reset token not found")

        orm_token.used = True

        session.flush()

    # ==========================================================
    # REFRESH TOKENS
    # ==========================================================

    def create_refresh_token(
        self,
        *,
        session:Session,
        user_id: int,
        token_hash: str,
        family_id:str,
        expires_at: datetime 
    ) -> int:

        orm_token = RefreshTokenORM(
            user_id=user_id,
            token_hash=token_hash,
            family_id=family_id,
            expires_at=expires_at,
            used=False,
            revoked=False
        )

        session.add(orm_token)

        session.flush()

        return orm_token.id

    # ----------------------------------------------------------

    def get_refresh_token(
        self,
        *,
        session:Session,
        token_hash: str
    ) -> RefreshTokenRecord:

        stmt = (
            select(RefreshTokenORM)
            .where(RefreshTokenORM.token_hash == token_hash)
            .with_for_update()
        )

        orm_token = session.execute(stmt).scalar_one_or_none()

        if not orm_token:
            raise NotFoundError("Refresh token not found")

        return RefreshTokenRecord(
            id=orm_token.id,
            user_id=orm_token.user_id,
            token_hash=orm_token.token_hash,
            expires_at=orm_token.expires_at,
            used=orm_token.used,
            revoked=orm_token.revoked,
            family_id=orm_token.family_id,
        )

    # ----------------------------------------------------------

    def mark_refresh_token_used(
        self,
        *,
        session:Session,
        token_id: int
    ) -> None:

        stmt = select(RefreshTokenORM).where(
            RefreshTokenORM.id == token_id
        )

        orm_token = session.execute(stmt).scalar_one_or_none()

        if not orm_token:
            raise NotFoundError("Refresh token not found")

        orm_token.used = True

        session.flush()

    def revoke_refresh_token(
    self,
    *,
    session: Session,
    token_id: int
) -> None:

        stmt = select(RefreshTokenORM).where(
            RefreshTokenORM.id == token_id
        )

        orm_token = session.execute(stmt).scalar_one_or_none()

        if not orm_token:
            raise NotFoundError("Refresh token not found")

        orm_token.revoked = True

        session.flush()        
    
    def revoke_token_family(
    self,
    *,
    session: Session,
    family_id: str
) -> None:

        stmt = select(RefreshTokenORM).where(
            RefreshTokenORM.family_id == family_id
        )

        tokens = session.execute(stmt).scalars().all()

        for token in tokens:
            token.revoked = True

        session.flush()
    
    def revoke_tokens_by_user(
    self,
    *,
    session: Session,
    user_id: int
) -> None:

        stmt = select(RefreshTokenORM).where(
            RefreshTokenORM.user_id == user_id
        )

        tokens = session.execute(stmt).scalars().all()

        for token in tokens:
            token.revoked = True

        session.flush()



    
    
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
    
    
   