from abc import ABC, abstractmethod
from typing import List, Optional,Dict
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy.orm import Session

from domain.user import User
from domain.task import Task
from domain.project import Project
from domain.audit_log import AuditLog
from modules.notifications.domain.models import Notification
from modules.billing.domain.models import Subscription

# ================================
# 🔐 DTOs
# ================================

@dataclass
class PasswordResetTokenRecord:
    """
    DTO لقراءة بيانات reset token
    """
    id: int
    user_id: int
    token_hash: str
    expires_at: datetime
    used: bool


@dataclass
class RefreshTokenRecord:
    id: int
    user_id: int
    token_hash: str
    expires_at: datetime
    used: bool
    revoked: bool
    family_id: str


# ================================
# 🧱 Base Storage Contract
# ================================

class BaseStorage(ABC):
    """
    Clean Storage Contract (Final Version)

    Principles:
    - Storage does NOT control transactions
    - Storage returns Domain models (NOT ORM)
    - Service handles business logic
    - Supports pagination & isolation
    """

    

    # ==========================================================
    # USERS
    # ==========================================================

    @abstractmethod
    def create_user(
        self,
        *,
        session,
        user: User
    ) -> User:
        """
        Persist a new user.
        Must assign ID.
        """

    @abstractmethod
    def update_user(
        self,
        *,
        session,
        user: User
    ) -> User:
        """
        Update user fields.
        """

    @abstractmethod
    def get_user_by_email(
        self,
        *,
        session,
        email: str
    ) -> User:
        """
        Retrieve user by email.
        """

    @abstractmethod
    def get_user_by_id(
        self,
        *,
        session,
        user_id: int
    ) -> User:
        """
        Retrieve user by ID.
        """

    @abstractmethod
    def update_user_password(
        self,
        *,
        session,
        user_id: int,
        password_hash: str,
    ) -> None:
        """
        Update password hash.
        """

    # ==========================================================
    # PASSWORD RESET TOKENS
    # ==========================================================

    @abstractmethod
    def create_password_reset_token(
        self,
        *,
        session,
        user_id: int,
        token_hash: str,
        expires_at: datetime,
    ) -> int:
        """
        Persist password reset token.
        """

    @abstractmethod
    def get_password_reset_token(
        self,
        *,
        session,
        token_hash: str,
    ) -> PasswordResetTokenRecord:
        """
        Retrieve reset token by hash.
        """

    @abstractmethod
    def mark_password_reset_token_used(
        self,
        *,
        session,
        token_id: int
    ) -> None:
        """
        Mark reset token as used.
        """

    # ==========================================================
    # REFRESH TOKENS
    # ==========================================================

    @abstractmethod
    def create_refresh_token(
        self,
        *,
        session,
        user_id: int,
        token_hash: str,
        family_id: str,
        expires_at: datetime,
    ) -> int:
        """
        Persist refresh token.
        """

    @abstractmethod
    def get_refresh_token(
        self,
        *,
        session,
        token_hash: str,
    ) -> RefreshTokenRecord:
        """
        Retrieve refresh token.
        """

    @abstractmethod
    def mark_refresh_token_used(
        self,
        *,
        session,
        token_id: int
    ) -> None:
        """
        Mark token as used.
        """

    @abstractmethod
    def revoke_refresh_token(
        self,
        *,
        session,
        token_id: int
    ) -> None:
        """
        Revoke single token.
        """

    @abstractmethod
    def revoke_token_family(
        self,
        *,
        session,
        family_id: str
    ) -> None:
        """
        Revoke all tokens in family.
        """

    @abstractmethod
    def revoke_tokens_by_user(
        self,
        *,
        session,
        user_id: int
    ) -> None:
        """
        Revoke all user tokens.
        """

    @abstractmethod
    def create_audit_log(
        self,
        session,
        log:AuditLog,

    )-> AuditLog:
        pass    
