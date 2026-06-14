from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Plan:
    id: int
    name: str
    price: float
    max_projects: Optional[int]


@dataclass
class Subscription:
    id: Optional[int]
    user_id: int
    plan_id: int
    status: str
    start_date: datetime
    end_date: Optional[datetime]