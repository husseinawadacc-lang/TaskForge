# ==========================================
# TaskService (FINAL RBAC VERSION)
# ==========================================

from typing import Tuple, List
from modules.tasks.domain.task import Task
from modules.tasks.storage.task_storage import TaskStorage
from core.unit_of_work import UnitOfWork
from modules.ai.service.ai_service import AIService
from modules.project.service.project_service import ProjectService
from modules.audit.services.audit_service import AuditService
from core.logger import get_logger
from core.exceptions import (
    TaskNotFoundError,
    InvalidPaginationError,
    NotFoundError,)
from modules.notifications.service.notification_service import NotificationService
logger = get_logger(__name__)


class TaskService:
    """
    TaskService (RBAC Final)

    Responsibilities:
    - Manage task lifecycle
    - Enforce RBAC via ProjectService
    - Prevent IDOR
    - Handle pagination
    - Integrate AI (priority)
    """

    DEFAULT_LIMIT = 20
    MAX_LIMIT = 100

    def __init__(
        self,
        task_storage: TaskStorage,
        uow: UnitOfWork,
        project_service: ProjectService,
        audit_service:AuditService,
        notification_service: NotificationService,
    ):
        self.task_storage = task_storage
        self.uow = uow
        self.project_service = project_service
        self.ai = AIService()
        self.audit =audit_service
        self.notification = notification_service
    # =====================================================
    # CREATE TASK
    # =====================================================
    def create_task(
        self,
        *,
        title: str,
        description: str,
        owner_id: int,
        project_id: int,
        parent_id: int | None = None,
    ) -> Task:

        with self.uow as session:

            # 🔥 RBAC: only admin / member
            project= self.project_service.get_project_in_session(
                session=session,
                project_id=project_id,
                requester_id=owner_id,
                            )
            self.project_service.require_role(
                session=session,
                project=project,
                user_id=owner_id,
                allowed_roles=["admin","member"]
            )
            if parent_id is not None:
                self.task_storage.get_task(
                    session=session,
                    task_id=parent_id
                )
            priority = self.ai.suggest_priority(title)

            task = Task(
                id=None,
                title=title,
                description=description,
                owner_id=owner_id,
                project_id=project_id,
                completed=False,
                priority=priority,
                parent_id=parent_id,
            )
            created = self.task_storage.create_task(
                    session=session,
                    task=task,
                )
            
            

            # 🔥 AUDIT
            self.audit.log(
                session=session,
                user_id=owner_id,
                action="task_created",
                resource_type="task",
                resource_id=created.id,
                details={
                    "title": created.title,
                    "project_id": project_id,
                },
            )


            # 🔥 Notification (اختياري)
            # 🔥 Future: trigger notification if task assigned to another user
        
        return created
    # =====================================================
    # GET TASK
    # =====================================================
    def get_task(
        self,
        *,
        task_id: int,
        requester_id: int,
    ) -> Task:

        with self.uow as session:

            try:
                task = self.task_storage.get_task(
                    session=session,
                    task_id=task_id,
                )
            except NotFoundError:
                raise TaskNotFoundError()

            # 🔥 RBAC: viewer+
            project= self.project_service.get_project_in_session(
                session=session,
                project_id=task.project_id,
                requester_id=requester_id,
                            )
          
            self.project_service.require_role(
                session=session,
                project=project,
                user_id=requester_id,
                allowed_roles=["admin", "member", "viewer"],
            )


            return task

    # =====================================================
    # UPDATE TASK
    # =====================================================
    def update_task(
        self,
        *,
        task_id: int,
        requester_id: int,
        title: str | None = None,
        description: str | None = None,
        completed: bool | None = None,
        priority: str | None = None,
    ) -> Task:

        with self.uow as session:

            try:
                existing = self.task_storage.get_task(
                    session=session,
                    task_id=task_id,
                )
            except NotFoundError:
                raise TaskNotFoundError()

            # 🔥 RBAC: only admin / member
            project= self.project_service.get_project_in_session(
                session=session,
                project_id=existing.project_id,
                requester_id=requester_id,
                            )
          
            self.project_service.require_role(
                session=session,
                project=project,
                user_id=requester_id,
                allowed_roles=["admin", "member"],
            )

            task = Task(
                id=task_id,
                title=(title if title is not None else existing.title),
                description=(description if description is not None else existing.description),
                completed=(completed if completed is not None else existing.completed),
                priority=(priority if priority is not None else existing.priority),
                owner_id=existing.owner_id,
                project_id=existing.project_id,
            )

            updated = self.task_storage.update_task(
                session=session,
                task=task,
            )

            # 🔥 AUDIT
            self.audit.log(
                session=session,
                user_id=requester_id,
                action="task_updated",
                resource_type="task",
                resource_id=task_id,
                details={
                    "title": title,
                    "completed": completed,
                    "priority": priority,
                },)
            
            
            return updated

    # =====================================================
    # DELETE TASK
    # =====================================================
    def delete_task(
        self,
        *,
        task_id: int,
        requester_id: int,
    ) -> None:

        with self.uow as session:

            try:
                task = self.task_storage.get_task(
                    session=session,
                    task_id=task_id,
                )
            except NotFoundError:
                raise TaskNotFoundError()

            # 🔥 RBAC: only admin
            project= self.project_service.get_project_in_session(
                session=session,
                project_id=task.project_id,
                requester_id=requester_id,
                            )
          
            self.project_service.require_role(
                session=session,
                project=project,
                user_id=requester_id,
                allowed_roles=["admin"],
            )
            self.task_storage.delete_task(
                session=session,
                task_id=task_id,
            )

            # 🔥 AUDIT
            self.audit.log(
                session=session,
                user_id=requester_id,
                action="task_deleted",
                resource_type="task",
                resource_id=task_id,
            )

    # =====================================================
    # LIST TASKS
    # =====================================================
    def list_tasks(
        self,
        *,
        owner_id: int,
        project_id: int,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Tuple[List[Task], int]:

        limit = limit or self.DEFAULT_LIMIT
        offset = offset or 0

        if limit < 1:
            raise InvalidPaginationError("limit must be >= 1")

        if limit > self.MAX_LIMIT:
            raise InvalidPaginationError("limit too large")

        if offset < 0:
            raise InvalidPaginationError("offset must be >= 0")

        with self.uow as session:

            # 🔥 RBAC: viewer+
            project= self.project_service.get_project_in_session(
                session=session,
                project_id=project_id,
                requester_id=owner_id,
                
                            )
          

            self.project_service.require_role(
                session=session,
                project=project,
                user_id=owner_id,
                allowed_roles=["admin", "member", "viewer"],
            )

            items = self.task_storage.list_tasks(
                session=session,
                owner_id=owner_id,
                project_id=project_id,
                limit=limit,
                offset=offset,
            )

            total = self.task_storage.count_tasks(
                session=session,
                owner_id=owner_id,
                project_id=project_id,
            )

            return items, total
        
    def generate_subtasks_for_task(
        self,
        *,
        task_id: int,
        title: str,
        owner_id: int,
        project_id: int,
    ):
        

        with self.uow as session:

            # make sure task is found

            parent= self.task_storage.get_task(
                session=session,
                task_id=task_id,
            )
            project = self.project_service.get_project_in_session(
            session=session,
            project_id=project_id,
            requester_id=owner_id,
        )

            self.project_service.require_role(
            session=session,
            project=project,
            user_id=owner_id,
            allowed_roles=["admin", "member"],
        )
            subtasks= self.ai.generate_subtasks(title)

            for sub in subtasks:
                task = Task(
                    id=None,
                    title=sub,
                    description="",
                    owner_id=owner_id,
                    project_id=project_id,
                    parent_id=task_id,  # 🔥 الربط
                    completed=False,
                    priority="low",
                )

                self.task_storage.create_task(session=session, task=task) 

        

    def _build_task_tree(self, session, task: Task, visited=None) -> Task:

        if task.id is None:
            return task

        if visited is None:
            visited = set()

        if task.id in visited:
            return task

        visited.add(task.id)

        children = self.task_storage.get_tasks_by_parent(
            session=session,
            parent_id=task.id,
        )

        task.subtasks = [
            self._build_task_tree(session, child, visited)
            for child in children
        ]

        return task

    def get_task_with_subtasks(
        self,
        *,
        task_id: int,
        requester_id: int,
    ) -> Task:

        with self.uow as session:

            try:
                task = self.task_storage.get_task(
                    session=session,
                    task_id=task_id,
                )
            except NotFoundError:
                raise TaskNotFoundError()    

            # 🔥 RBAC (مهم جدًا)
            project = self.project_service.get_project_in_session(
                session=session,
                project_id=task.project_id,
                requester_id=requester_id,
            )

            self.project_service.require_role(
                session=session,
                project=project,
                user_id=requester_id,
                allowed_roles=["admin", "member", "viewer"],
            )

            return self._build_task_tree(session, task)
        
    def assign_task(
        self,
        *,
        task_id: int,
        assigned_user_id: int,
        actor_id: int,
    ) -> Task:

            with self.uow as session:

                task = self.task_storage.get_task(
                    session=session,
                    task_id=task_id,
                )

                project = self.project_service.get_project_in_session(
                    session=session,
                    project_id=task.project_id,
                    requester_id=actor_id,
                )

                self.project_service.require_role(
                    session=session,
                    project=project,
                    user_id=actor_id,
                    allowed_roles=["admin", "member"],
                )

                if task.owner_id == assigned_user_id:
                    return task
                task.owner_id = assigned_user_id
                updated = self.task_storage.update_task(
                    session=session,
                    task=task,
                )

                # 🔥 AUDIT
                self.audit.log(
                    session=session,
                    user_id=actor_id,
                    action="task_assigned",
                    resource_type="task",
                    resource_id=task_id,
                    details={"assigned_to": assigned_user_id},
                )

                # 🔥 Notification (نفس transaction)
                self.notification.notify_task_assigned(
                    task=updated,
                    assigned_user_id=assigned_user_id,
                    actor_id=actor_id,
                    
                )

                return updated