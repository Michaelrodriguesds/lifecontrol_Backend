# app/models/goal.py
from beanie import Document
from pydantic import Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class GoalStatus(str, Enum):
    active    = "active"
    completed = "completed"
    paused    = "paused"
    cancelled = "cancelled"


class GoalCategory(str, Enum):
    vehicle    = "vehicle"
    technology = "technology"
    travel     = "travel"
    education  = "education"
    health     = "health"
    investment = "investment"
    other      = "other"


# ⚠️ PROBLEMA CORRIGIDO:
# priority era int (1-5) mas o frontend Angular envia strings
# ('low','medium','high','critical'). Mudamos para string.
class GoalPriority(str, Enum):
    low      = "low"
    medium   = "medium"
    high     = "high"
    critical = "critical"


class Goal(Document):
    user_id:        str
    title:          str
    description:    Optional[str]      = None
    category:       Optional[str]      = None
    target_amount:  float
    current_amount: float              = 0.0
    deadline:       Optional[datetime] = None
    status:         GoalStatus         = GoalStatus.active
    icon:           Optional[str]      = None
    color:          Optional[str]      = "#6366f1"
    priority:       str                = "medium"   # string livre para compatibilidade
    tags:           List[str]          = []
    created_at:     datetime           = Field(default_factory=datetime.utcnow)
    updated_at:     datetime           = Field(default_factory=datetime.utcnow)

    @property
    def progress_percentage(self) -> float:
        if self.target_amount == 0:
            return 0
        return min((self.current_amount / self.target_amount) * 100, 100)

    class Settings:
        name = "goals"


class GoalTransaction(Document):
    goal_id:          str
    user_id:          str
    amount:           float
    description:      Optional[str] = None
    transaction_type: str           = "deposit"
    date:             datetime      = Field(default_factory=datetime.utcnow)
    created_at:       datetime      = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "goal_transactions"