from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.expense import ExpenseType


class ExpenseCreate(BaseModel):
    title: str
    amount: float = Field(gt=0)
    category_id: Optional[str] = None
    category_name: Optional[str] = None
    item_id: Optional[str] = None
    goal_id: Optional[str] = None
    expense_type: ExpenseType = ExpenseType.variable
    date: Optional[datetime] = None
    description: Optional[str] = None
    tags: List[str] = []
    is_recurring: bool = False
    recurrence_day: Optional[int] = None


class ExpenseUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None
    category_id: Optional[str] = None
    category_name: Optional[str] = None
    expense_type: Optional[ExpenseType] = None
    date: Optional[datetime] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
