from core.unit_of_work import UnitOfWork

def get_unit_of_work() -> UnitOfWork:
    """
    Provide UnitOfWork instance.

    Responsibilities:
    - Manage transactions across multiple repositories
    - Ensure atomicity of operations
    - Handle commit/rollback logic
    """
    return UnitOfWork()