from enum import Enum


class NotificationType(str, Enum):
    TASK_ASSIGNED = "task_assigned"
    TASK_UPDATED = "task_updated"
    PROJECT_INVITE = "project_invite"

    def label(self) -> str:
        return {
            self.TASK_ASSIGNED: "New Task Assigned",
            self.TASK_UPDATED: "Task Updated",
            self.PROJECT_INVITE: "Project Invitation",
        }[self]