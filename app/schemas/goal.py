# app/schemas/goal.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

# ⚠️ PROBLEMA CORRIGIDO:
# O modelo original usava priority: int (1-5) mas o frontend Angular
# envia strings: 'low', 'medium', 'high', 'critical'.
# Trocamos para um Enum de strings para evitar o erro 422.
class GoalPriority(str, Enum):
    low      = "low"
    medium   = "medium"
    high     = "high"
    critical = "critical"

from app.models.goal import GoalStatus, GoalCategory


class GoalCreate(BaseModel):
    title:         str
    description:   Optional[str]          = None
    category:      Optional[str]          = None   # aceita string livre também
    target_amount: float                  = Field(gt=0)
    deadline:      Optional[datetime]     = None
    icon:          Optional[str]          = None
    color:         Optional[str]          = "#6366f1"
    priority:      GoalPriority           = GoalPriority.medium
    tags:          List[str]              = []


class GoalUpdate(BaseModel):
    title:         Optional[str]          = None
    description:   Optional[str]          = None
    category:      Optional[str]          = None
    target_amount: Optional[float]        = None
    deadline:      Optional[datetime]     = None
    status:        Optional[GoalStatus]   = None
    icon:          Optional[str]          = None
    color:         Optional[str]          = None
    priority:      Optional[GoalPriority] = None
    tags:          Optional[List[str]]    = None


class TransactionCreate(BaseModel):
    amount:           float           = Field(gt=0)
    description:      Optional[str]   = None
    # ⚠️ PROBLEMA CORRIGIDO:
    # O frontend mandava o campo como "type" mas o backend esperava
    # "transaction_type". Agora aceitamos os dois nomes via alias.
    transaction_type: str             = "deposit"   # deposit | withdrawal
    date:             Optional[datetime] = None