from abc import ABC, abstractmethod
from typing import List, Optional,Dict
from datetime import datetime
from dataclasses import dataclass


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

