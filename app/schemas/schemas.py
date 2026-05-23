from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Any
from datetime import datetime
from enum import Enum


# ─── AUTH SCHEMAS ────────────────────────────────────────────────────────────
class UserRegister(BaseModel):
    email: EmailStr
    name: str
    password: str = Field(min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class UserOut(BaseModel):
    id: str
    email: str
    name: str
    is_active: bool


# ─── GOAL SCHEMAS ────────────────────────────────────────────────────────────
class GoalCreate(BaseModel):
    title: str
    description: Optional[str] = None
    target_amount: float = Field(gt=0)
    priority: str = "medium"
    category: Optional[str] = None
    icon: Optional[str] = "target"
    color: Optional[str] = "#6366f1"
    deadline: Optional[datetime] = None


class GoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    target_amount: Optional[float] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    category: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    deadline: Optional[datetime] = None


class TransactionCreate(BaseModel):
    amount: float = Field(gt=0)
    type: str = "deposit"  # deposit | withdrawal
    description: Optional[str] = None
    date: Optional[datetime] = None


# ─── EXPENSE SCHEMAS ─────────────────────────────────────────────────────────
class ExpenseCreate(BaseModel):
    title: str
    amount: float = Field(gt=0)
    category_id: Optional[str] = None
    category_name: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    tags: List[str] = []
    is_recurring: bool = False


class ExpenseUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None
    category_id: Optional[str] = None
    category_name: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    tags: Optional[List[str]] = None


# ─── CATEGORY SCHEMAS ────────────────────────────────────────────────────────
class CategoryCreate(BaseModel):
    name: str
    color: str = "#6366f1"
    icon: str = "tag"


# ─── ITEM SCHEMAS ────────────────────────────────────────────────────────────
class ItemCreate(BaseModel):
    name: str
    type: str = "custom"
    description: Optional[str] = None
    purchase_price: Optional[float] = None
    current_value: Optional[float] = None
    purchase_date: Optional[datetime] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    color: Optional[str] = "#6366f1"
    icon: Optional[str] = "box"
    tags: List[str] = []
    notes: Optional[str] = None


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    current_value: Optional[float] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None


# ─── FUTURE EXPENSE SCHEMAS ──────────────────────────────────────────────────
class FutureExpenseCreate(BaseModel):
    title: str
    expected_amount: float = Field(gt=0)
    paid_amount: float = 0.0
    category_name: Optional[str] = None
    priority: str = "medium"
    due_date: Optional[datetime] = None
    description: Optional[str] = None


class FutureExpenseUpdate(BaseModel):
    title: Optional[str] = None
    expected_amount: Optional[float] = None
    paid_amount: Optional[float] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    is_paid: Optional[bool] = None
    description: Optional[str] = None


# ─── NOTE SCHEMAS ────────────────────────────────────────────────────────────
class NoteCreate(BaseModel):
    title: str
    content: Optional[str] = None
    type: str = "free"
    checklist: List[dict] = []
    tags: List[str] = []
    color: Optional[str] = "#1e1e2e"
    is_pinned: bool = False
    reminder_at: Optional[datetime] = None


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    checklist: Optional[List[dict]] = None
    tags: Optional[List[str]] = None
    color: Optional[str] = None
    is_pinned: Optional[bool] = None
    reminder_at: Optional[datetime] = None
