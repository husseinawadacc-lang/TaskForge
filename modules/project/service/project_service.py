# ==========================================
# ProjectService (FINAL PRO VERSION)
# ==========================================

from typing import List
from modules.project.domain.project import Project
from modules.user.storage.user_storage import UserStorage 
from modules.billing.service.billing_service import BillingService
from modules.project.storage.project_storage import ProjectStorage
from modules.project.storage.project_member_storage import ProjectMemberStorage
from core.unit_of_work import UnitOfWork
from modules.audit.services.audit_service import AuditService
from core.exceptions import NotFoundError,PermissionDeniedError


class ProjectService:
    """
    ProjectService

    Responsibilities
    ----------------
    - Manage project lifecycle (CRUD)
    - Manage project members (invite / remove)
    - Enforce access control (RBAC)
    - Protect against IDOR (hide existence)
    - Coordinate storage operations
    - Use UnitOfWork for transactions

    IMPORTANT DESIGN RULES
    ----------------------
    1) Owner is NOT just a role → special case
    2) RBAC is used for shared access (admin/member/viewer)
    3) All access control MUST go through this service
    """

    def __init__(
            self, project_storage: ProjectStorage,
             member_storage: ProjectMemberStorage,
             user_storage: UserStorage,
              uow: UnitOfWork,
            audit_service:AuditService, billing_service:BillingService):
        self.project_storage = project_storage
        self.member_storage= member_storage
        self.user_storage= user_storage
        self.uow = uow
        self.audit=audit_service
        self.billing=billing_service

    # =====================================================
    # CREATE PROJECT
    # =====================================================
    def create_project(
        self,
        *,
        owner_id: int,
        name: str,
    ) -> Project:
        """
        Create new project.

        Flow:
        - Create Project entity
        - Persist via storage
        - Storage automatically:
            ✔ assigns ID
            ✔ adds owner as member (role=admin)
        """

        with self.uow as session:
            # 🔥 count current projects
            current_projects =self.project_storage.count_projects(
                    session=session,
                    owner_id=owner_id
                )
        

            # 🔥 billing check
            if not self.billing.can_create_project(
                session=session,
                user_id=owner_id,
                current_projects=current_projects
            ):
                raise PermissionDeniedError()
            
        

            project = Project(
                id=None,
                name=name,
                owner_id=owner_id,
            )
            created = self.project_storage.create_project(
                session=session,
                project=project,
            )

            self.audit.log(
                session=session,
                user_id=owner_id,
                action="project_created",
                resource_type="project",
                resource_id=created.id,
                details={"name": name},
            )

            return created
    # =====================================================
    # GET PROJECT (RBAC)
    # =====================================================
    def get_project(
        self,
        *,
        project_id: int,
        requester_id: int,
    ) -> Project:
        """
        Retrieve project with RBAC.

        Access:
        - owner ✔
        - admin ✔
        - member ✔
        - viewer ✔
        - others → NotFound (Anti-IDOR)
        """
        with self.uow as session:
          return   self.get_project_in_session(
            session=session,
            project_id=project_id,
            requester_id=requester_id
                    )


    # =====================================================
    # LIST PROJECTS
    # =====================================================
    def list_projects(
        self,
        *,
        owner_id: int,
    ) -> List[Project]:
        """
        List projects owned by user.

        NOTE:
        - Currently returns owned projects only
        - Later: include shared projects
        """

        with self.uow as session:

            return self.project_storage.list_projects(
                session=session,
                owner_id=owner_id,
            )

    # =====================================================
    # DELETE PROJECT (OWNER ONLY)
    # =====================================================
    def delete_project(
        self,
        *,
        project_id: int,
        requester_id: int,
    ) -> None:
        """
        Delete project.

        Rules:
        - ONLY owner can delete
        - RBAC is NOT used here (owner is special case)
        """

        with self.uow as session:

            project = self.project_storage.get_project(
                session=session,
                project_id=project_id,
            )

            # 🔴 owner-only rule
            if project.owner_id != requester_id:
                raise NotFoundError("Project not found")

            self.project_storage.delete_project(
                session=session,
                project_id=project_id,
            )

            self.audit.log(
                session=session,
                user_id=requester_id,
                action="project_deleted",
                resource_type="project",
                resource_id=project_id,
            )

    # =====================================================
    # ADD MEMBER (OWNER ONLY)
    # =====================================================
    def add_member(
        self,
        *,
        project_id: int,
        owner_id: int,
        user_id: int,
        role: str = "member",
    ) -> None:
        """
        Add user to project.

        Rules:
        - ONLY owner can invite
        - User must exist
        - Role can be:
            admin / member / viewer
        """

        with self.uow as session:

            project = self.project_storage.get_project(
                session=session,
                project_id=project_id,
            )

            # 🔴 owner-only
            if project.owner_id != owner_id:
                raise NotFoundError("Project not found")

            # 🔍 ensure user exists
            self.user_storage.get_user_by_id(
                session=session,
                user_id=user_id,
            )

            self.member_storage.add_project_member(
                session=session,
                project_id=project_id,
                user_id=user_id,
                role=role,
            )

            self.audit.log(
                session=session,
                user_id=owner_id,
                action="member_added",
                resource_type="project",
                resource_id=project_id,
                details={
                    "target_user_id": user_id,
                    "role": role,
                },
            )

    # =====================================================
    # REMOVE MEMBER (OWNER ONLY)
    # =====================================================
    def remove_member(
        self,
        *,
        project_id: int,
        owner_id: int,
        user_id: int,
    ) -> None:
        """
        Remove user from project.

        Rules:
        - ONLY owner can remove
        - Owner cannot remove himself
        """

        with self.uow as session:

            project = self.project_storage.get_project(
                session=session,
                project_id=project_id,
            )

            # 🔴 owner-only
            if project.owner_id != owner_id:
                raise NotFoundError("Project not found")

            # ❗ prevent removing owner
            if user_id == owner_id:
                raise NotFoundError("Project not found")

            self.member_storage.remove_project_member(
                session=session,
                project_id=project_id,
                user_id=user_id,
            )

            self.audit.log(
                session=session,
                user_id=owner_id,
                action="member_removed",
                resource_type="project",
                resource_id=project_id,
                details={"target_user_id": user_id},
            )

    # =====================================================
    # RBAC CORE (IMPORTANT 🔥)
    # =====================================================
    def require_role(
        self,
        *,
        session,
        project:Project,
        user_id: int,
        allowed_roles: list[str],
    ) -> None:
        """
        Central RBAC enforcement.

        Rules:
        - Owner ALWAYS allowed (bypass)
        - Otherwise check member role
        - If not allowed → NotFound (Anti-IDOR)

        Why NotFound?
        - Prevents resource enumeration attacks
        """

           # 🟢 owner bypass
        if project.owner_id == user_id:
            return

        project_id = project.id
        if project_id is None:
            raise NotFoundError("Project not found")

        # 🔍 get role
        role = self.member_storage.get_project_member_role(
            session=session,
            project_id=project_id,
            user_id=user_id,
        )

        # ❌ not member
        if role is None:
            raise NotFoundError("Project not found")

        # ❌ role not allowed
        if role not in allowed_roles:
            raise NotFoundError("Project not found")
        
    def list_members(
        self,
        *,
        project_id: int,
        requester_id: int,
    ) -> dict[int, str]:

        with self.uow as session:

            project = self.project_storage.get_project(
                session=session,
                project_id=project_id,
            )

            self.require_role(
                session=session,
                project=project,
                user_id=requester_id,
                allowed_roles=["admin", "member", "viewer"],
            )

            return self.member_storage.list_project_members(
                session=session,
                project_id=project_id,
            )    
        
    def get_project_in_session(
    self,
    *,
    session,
    project_id: int,
    requester_id: int,
    ) -> Project:

        project = self.project_storage.get_project(
            session=session,
            project_id=project_id,
        )

        self.require_role(
            session=session,
            project=project,
            user_id=requester_id,
            allowed_roles=["admin", "member", "viewer"],
        )

        return project    