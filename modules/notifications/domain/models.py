from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Notification:
    id: Optional[int]
    user_id: int
    type: str
    title: str
    message: str
    is_read: bool = False
    created_at: Optional[datetime] = None
    task_id: Optional[int] = None
    project_id: Optional[int] = None