
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from modules.user.domain.user import User
from db.models.user import UserORM
from sqlalchemy.exc import IntegrityError
from core.exceptions import NotFoundError,ConflictError


class UserStorage:

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

   