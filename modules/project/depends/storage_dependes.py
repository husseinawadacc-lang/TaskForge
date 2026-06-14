
from modules.project.storage.project_storage import (
    ProjectStorage,
)
from modules.project.storage.project_member_storage import (
    ProjectMemberStorage,
)


def get_project_storage():
    return ProjectStorage()


def get_project_member_storage():
    return ProjectMemberStorage()