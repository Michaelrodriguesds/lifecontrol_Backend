# app/schemas/work_day.py
from pydantic import BaseModel, Field
from typing import Optional


class WorkDayCreate(BaseModel):
    date:       str            # YYYY-MM-DD
    worked:     bool  = True
    fueled:     bool  = False
    pnr_amount: float = Field(default=0.0, ge=0)
    notes:      Optional[str] = None


class WorkDayUpdate(BaseModel):
    worked:     Optional[bool]  = None
    fueled:     Optional[bool]  = None
    pnr_amount: Optional[float] = None
    notes:      Optional[str]   = None