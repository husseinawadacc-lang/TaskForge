from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NotificationOut(BaseModel):
    id: int
    type: str
    title: str
    message: str
    is_read: bool
    task_id: Optional[int]
    project_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True