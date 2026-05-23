from beanie import Document
from typing import Optional
from datetime import datetime
from enum import Enum


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class FutureExpense(Document):
    user_id: str
    title: str
    predicted_amount: float
    paid_amount: float = 0.0
    due_date: Optional[datetime] = None
    priority: Priority = Priority.medium
    category_id: Optional[str] = None
    category_name: Optional[str] = None
    description: Optional[str] = None
    is_paid: bool = False
    paid_at: Optional[datetime] = None
    item_id: Optional[str] = None
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    @property
    def remaining_amount(self) -> float:
        return max(self.predicted_amount - self.paid_amount, 0)

    class Settings:
        name = "future_expenses"
