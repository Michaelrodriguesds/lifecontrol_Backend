from beanie import Document
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ExpenseType(str, Enum):
    fixed = "fixed"
    variable = "variable"
    investment = "investment"
    emergency = "emergency"


class Expense(Document):
    user_id: str
    title: str
    amount: float
    category_id: Optional[str] = None
    category_name: Optional[str] = None
    item_id: Optional[str] = None   # Vinculado a um item
    goal_id: Optional[str] = None   # Vinculado a uma meta
    expense_type: ExpenseType = ExpenseType.variable
    date: datetime = datetime.utcnow()
    description: Optional[str] = None
    tags: List[str] = []
    receipt_url: Optional[str] = None
    is_recurring: bool = False
    recurrence_day: Optional[int] = None
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Settings:
        name = "expenses"
