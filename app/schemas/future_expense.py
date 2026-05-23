from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.future_expense import Priority


class FutureExpenseCreate(BaseModel):
    title: str
    predicted_amount: float = Field(gt=0)
    due_date: Optional[datetime] = None
    priority: Priority = Priority.medium
    category_id: Optional[str] = None
    category_name: Optional[str] = None
    description: Optional[str] = None
    item_id: Optional[str] = None


class FutureExpenseUpdate(BaseModel):
    title: Optional[str] = None
    predicted_amount: Optional[float] = None
    paid_amount: Optional[float] = None
    due_date: Optional[datetime] = None
    priority: Optional[Priority] = None
    is_paid: Optional[bool] = None
    description: Optional[str] = None
