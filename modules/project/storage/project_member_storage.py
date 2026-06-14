from sqlalchemy import select, func
from db .models.project_member import ProjectMemberORM
from sqlalchemy.exc import IntegrityError
from utils.exceptions import NotFoundError,ConflictError

class ProjectMemberStorage:
# ==========================================================
    # PROJECT  MEMBER OPERATIONS
    # ==========================================================

    def add_project_member(
        self,
        *,
        session,
        project_id: int,
        user_id: int,
        role: str = "member",
    ) -> None:

        orm = ProjectMemberORM(
            project_id=project_id,
            user_id=user_id,
            role=role,
        )
        try:
            session.add(orm)
            session.flush()  
        except IntegrityError:
            raise ConflictError("member already exists")    


    def remove_project_member(
        self,
        *,
        session,
        project_id: int,
        user_id: int,
    ) -> None:

        stmt = select(ProjectMemberORM).where(
            ProjectMemberORM.project_id == project_id,
            ProjectMemberORM.user_id == user_id,
        )

        orm = session.execute(stmt).scalar_one_or_none()

        if orm:
            session.delete(orm)   
            session.flush()
             

    def list_project_members(
        self,
        *,
        session,
        project_id: int,
    ) -> dict[int, str]:

        stmt = select(
            ProjectMemberORM.user_id,
            ProjectMemberORM.role
        ).where(
            ProjectMemberORM.project_id == project_id
        )

        rows = session.execute(stmt).all()

        return {user_id: role for user_id, role in rows}
    
    def get_project_member_role(
        self,
        *,
        session,
        project_id: int,
        user_id: int,
    ) -> str | None:

        stmt = select(ProjectMemberORM.role).where(
            ProjectMemberORM.project_id == project_id,
            ProjectMemberORM.user_id == user_id,
        )

        return session.execute(stmt).scalar_one_or_none()
    
    def is_project_member(
        self,
        *,
        session,
        project_id: int,
        user_id: int,
    ) -> bool:

        stmt = select(ProjectMemberORM.user_id).where(
            ProjectMemberORM.project_id == project_id,
            ProjectMemberORM.user_id == user_id,
        )

        return session.execute(stmt).scalar_one_or_none() is not None  
    