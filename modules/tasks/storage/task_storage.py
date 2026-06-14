from typing import List
from utils.exceptions import NotFoundError,ConflictError

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from domain.task import Task
from db.models.task import TaskORM

class TaskStorage:

    # =========================================================
    # MAPPER HELPER
    # ========================================================
    def _map_task(self,orm: TaskORM) -> Task:
        return Task(
            id=orm.id,
            title=orm.title,
            description=orm.description,
            owner_id=orm.owner_id,
            project_id=orm.project_id,
            parent_id=orm.parent_id,
            completed=orm.completed,
            created_at=orm.created_at,
            priority=orm.priority,
        )    

    # ==========================================================
    # TASK OPERATIONS
    # ==========================================================
    def create_task(
        self,
        *,
        session: Session,
        task: Task
    ) -> Task:
        orm_task = TaskORM(
            title=task.title,
            description=task.description,
            owner_id=task.owner_id,
            project_id = task.project_id,
            parent_id =task.parent_id,
            completed=task.completed or False,
            created_at=task.created_at or None,
            priority=task.priority or "low",
        )

        session.add(orm_task)
        session.flush()

        return self._map_task(orm_task)

    # ----------------------------------------------------------

    def get_task(self, *, session: Session, task_id: int) -> Task:

        stmt = select(TaskORM).where(TaskORM.id == task_id)

        orm_task = session.execute(stmt).scalar_one_or_none()

        if not orm_task:
            raise NotFoundError("Task not found")

        return self._map_task(orm_task)
    # ----------------------------------------------------------

    def update_task(
        self,
        *,
        session: Session,
        task: Task
    ) -> Task:

        stmt = select(TaskORM).where(TaskORM.id == task.id)

        orm_task = session.execute(stmt).scalar_one_or_none()

        if not orm_task:
            raise NotFoundError("Task not found")
          
        
        if task.title is not None:
            orm_task.title = task.title

        if task.description is not None:
            orm_task.description = task.description

        if task.completed is not None:
            orm_task.completed = task.completed

        if task.priority is not None:
            orm_task.priority = task.priority
            orm_task.owner_id = task.owner_id

        session.flush()

        return self._map_task(orm_task)
    # ----------------------------------------------------------

    def delete_task(self, *, session:Session, task_id: int) -> None:

        stmt = select(TaskORM).where(TaskORM.id == task_id)

        orm_task = session.execute(stmt).scalar_one_or_none()

        if not orm_task:
            raise NotFoundError("Task not found")

        session.delete(orm_task)
        session.flush()
    # ==========================================================
    # PAGINATION
    # ==========================================================
    def list_tasks(
        self,
        *,
        session: Session,
        owner_id: int,
        project_id:int,
        limit: int,
        offset: int
    ) -> List[Task]:

        stmt = (
            select(TaskORM)
            .where(TaskORM.owner_id == owner_id,
                   TaskORM.project_id == project_id,
                   )
            .limit(limit)
            .offset(offset)
        )

        tasks = session.execute(stmt).scalars().all()

        return [self._map_task(t) for t in tasks
        ]

    # ----------------------------------------------------------

    def count_tasks(self, *, session:Session, owner_id: int,project_id:int) -> int:

        stmt = select(func.count()).where(TaskORM.owner_id == owner_id,
                                            TaskORM.project_id == project_id
                                          )

        return session.execute(stmt).scalar_one()
    
    # --------------------------------------------------------
    def get_tasks_by_parent(
            self, *, session, parent_id: int) -> List[Task]:
        stmt = select(TaskORM).where(TaskORM.parent_id == parent_id)

        tasks = session.execute(stmt).scalars().all()

        return [self._map_task(t) for t in tasks]    
