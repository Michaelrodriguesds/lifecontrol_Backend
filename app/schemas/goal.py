from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.goal import GoalStatus, GoalCategory


class GoalCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: GoalCategory = GoalCategory.other
    target_amount: float = Field(gt=0)
    deadline: Optional[datetime] = None
    icon: Optional[str] = None
    color: Optional[str] = "#6366f1"
    priority: int = Field(default=1, ge=1, le=5)
    tags: List[str] = []


class GoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[GoalCategory] = None
    target_amount: Optional[float] = None
    deadline: Optional[datetime] = None
    status: Optional[GoalStatus] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    priority: Optional[int] = None
    tags: Optional[List[str]] = None


class TransactionCreate(BaseModel):
    amount: float = Field(gt=0)
    description: Optional[str] = None
    transaction_type: str = "deposit"
    date: Optional[datetime] = None
