
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
from modules.auth.storage.auth_storage import AuthStorage
from modules.user.storage.user_storage import UserStorage
# ==========================================================
# STORAGE
# ==========================================================

from modules.billing.depends.dependencies import get_billing_service
from modules.notifications.dependencies import get_notification_service

# ==========================================================
# CORE SERVICES
# ==========================================================

from core.unit_of_work import UnitOfWork
from modules.auth.services.password_policy_service import PasswordPolicyService
from modules.audit.services.audit_service import AuditService
# ==========================================================
# BUSINESS SERVICES
# ==========================================================

from modules.auth.services.token_services import TokenService
from modules.auth.services.auth_service import AuthService
from modules.auth.services.password_reset_services import PasswordResetService
from modules.notifications.service.notification_service import NotificationService
from modules.audit.depends.dependencies import get_audit_service
from api.deps.uow_dep import get_unit_of_work


"""
auth_dep.py

🔥 المسؤوليات:
- استخراج المستخدم من JWT
- فرض authentication على endpoints
- تحويل أي TokenError → HTTP 401

🔥 مبدأ مهم:
❗ لا نعمل decode هنا
✔ كل التحقق يتم داخل jwt.py + token_service
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from modules.auth.services.auth_service import AuthService
from modules.auth.services.token_services import TokenService

from core.exceptions import TokenError
from modules.user.domain.user import User


    
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
    auth_storage= AuthStorage() ,
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
        auth_storage=auth_storage,
        uow=uow,
    )

# ==========================================================
# AuthService
# ==========================================================

def get_auth_service(
    auth_storage= AuthStorage() ,
    user_storage=UserStorage(),
    password_policy: PasswordPolicyService = Depends(get_password_policy_service),
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
        auth_storage=auth_storage,
        user_storage=user_storage,
        password_policy=password_policy,
        uow=uow,
        token_service=token_service,
        billing_service=billing_service,
    )


# ==========================================================
# Password Reset Service
# ==========================================================

def get_password_reset_service(
    auth_storage= AuthStorage() ,
    user_storage= UserStorage(),
    password_policy: PasswordPolicyService = Depends(get_password_policy_service),
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
        auth_storage=auth_storage,
        user_storage=user_storage,
        password_policy=password_policy,
        uow=uow,
    )


# ==========================================================
# Security Scheme (Bearer Token)
# ==========================================================

# 🔐 FastAPI هيتعامل مع Authorization: Bearer <token>
security = HTTPBearer()


# ==========================================================
# Get Current User (Full user object)
# ==========================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    """
    🔥 الهدف:
    استخراج المستخدم الحالي من التوكن

    =====================================================
    🔄 Flow النهائي (بعد الإصلاح)
    =====================================================

    1️⃣ استخراج التوكن من header
    2️⃣ تمرير التوكن إلى AuthService
    3️⃣ AuthService →
        → TokenService →
            → decode_and_verify_jwt (🔥 هنا كل السحر)
                ✔ verify signature
                ✔ check expiration
                ✔ check blacklist (logout)
                ✔ verify token type
    4️⃣ استخراج user_id
    5️⃣ تحميل المستخدم من DB
    6️⃣ التأكد إنه active
    7️⃣ إرجاع user

    =====================================================
    ❗ مهم جدًا:
    ❌ لا نعمل decode هنا
    ❌ لا نعمل blacklist check هنا
    ✔ كل ده يتم في jwt.py فقط
    =====================================================
    """

    token = credentials.credentials

    try:
        # 🔥 كل validation بيحصل تحت (token_service + jwt.py)
        user = auth_service.get_user_from_token(token)

        # 🛑 منع المستخدم غير المفعل
        if not user.is_active:
            raise TokenError("Inactive user")

        return user

    except TokenError:
        # 🔴 أي مشكلة في التوكن → Unauthorized
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ==========================================================
# Get Current User ID (Lightweight)
# ==========================================================

def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    token_service: TokenService = Depends(get_token_service),
) -> int:
    """
    🔥 الهدف:
    استخراج user_id فقط بدون تحميل user من DB

    =====================================================
    🔄 Flow
    =====================================================

    1️⃣ استخراج التوكن
    2️⃣ تمريره إلى TokenService
    3️⃣ TokenService →
        → decode_and_verify_jwt
            ✔ signature
            ✔ expiration
            ✔ blacklist (🔥 logout check)
            ✔ token type
    4️⃣ استخراج user_id (sub)
    5️⃣ إرجاعه

    =====================================================
    💡 يستخدم في:
    - endpoints performance-critical
    - لما مش محتاج user كامل
    =====================================================
    """

    token = credentials.credentials

    try:
        # 🔥 نفس source of truth
        user_id = token_service.validate_access_token(token)

        return user_id

    except TokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )
    
