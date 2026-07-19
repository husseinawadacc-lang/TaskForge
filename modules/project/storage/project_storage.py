from datetime import datetime,timezone
from typing import List,Dict
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from modules.project.domain.project import Project
from db.models.project import ProjectORM
from db.models.task import TaskORM
from db .models.project_member import ProjectMemberORM
from sqlalchemy.exc import IntegrityError
from core.exceptions import NotFoundError,ConflictError

class ProjectStorage:
    # ==========================================================
    # PROJECT OPERATIONS
    # ==========================================================

   

    def map_project(self, orm: ProjectORM) -> Project:
        return Project(
            id=orm.id,
            name=orm.name,
            owner_id=orm.owner_id,
            created_at=orm.created_at,
        )


    # ----------------------------------------------------------

    def create_project(
        self,
        *,
        session: Session,
        project: Project
    ) -> Project:

        orm_project = ProjectORM(
            name=project.name,
            owner_id=project.owner_id,
            created_at=datetime.now(timezone.utc))
        try:
            session.add(orm_project)
            session.flush()
        except IntegrityError as e:
                
            if "unique" in str(e).lower():
                raise ConflictError("project already exists") from e
    
    # 🔥 add owner 
        owner_member = ProjectMemberORM(
        project_id=orm_project.id,
        user_id=orm_project.owner_id,
        role="owner",)


        session.add(owner_member)
        session.flush()

       
        return self.map_project(orm_project)


    # ----------------------------------------------------------

    def get_project(
        self,
        *,
        session: Session,
        project_id: int
    ) -> Project:

        stmt = select(ProjectORM).where(ProjectORM.id == project_id)

        orm_project = session.execute(stmt).scalar_one_or_none()

        if not orm_project:
            raise NotFoundError("Project not found")

        return self.map_project(orm_project)


    # ----------------------------------------------------------

    def list_projects(
        self,
        *,
        session: Session,
        owner_id: int
    ) -> List[Project]:

        stmt = select(ProjectORM).join(ProjectMemberORM).where(ProjectMemberORM.user_id == owner_id)

        projects = session.execute(stmt).scalars().all()

        return [self.map_project(p) for p in projects]     

    # -------------------------------------------------------------

    def count_projects(
        self,
        *,
        session: Session,
        owner_id: int
    ) -> int:

        stmt = select(func.count()).select_from(ProjectORM).join(ProjectMemberORM).where(ProjectMemberORM.user_id == owner_id)

        return session.execute(stmt).scalar_one()

    # -------------------------------------------------------------
    def delete_project(
            self,
            *,
            session:Session,
            project_id:int,
    )  ->  None :
        stmt=select(ProjectORM).where(ProjectORM.id== project_id)
        orm_project = session.execute(stmt).scalar_one_or_none()
        if not orm_project:
            raise NotFoundError("project not found")
        
        tasks = session.execute(
        select(TaskORM).where(TaskORM.project_id == project_id)
        ).scalars().first()

        if tasks:
            raise ConflictError("Project has tasks")
        session.delete(orm_project)
        session.flush()
