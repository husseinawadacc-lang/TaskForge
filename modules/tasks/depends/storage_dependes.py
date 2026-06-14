from modules.tasks.storage.task_storage import TaskStorage


def get_task_storage() -> TaskStorage:
    return TaskStorage()