from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from modules.auth.domain.auth import (
    PasswordResetTokenRecord,
    RefreshTokenRecord)
from db.models.password_reset import PasswordResetTokenORM
from db.models.refresh_token import RefreshTokenORM
from sqlalchemy.exc import IntegrityError
from core.exceptions import NotFoundError,ConflictError


class AuthStorage:
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



    
   