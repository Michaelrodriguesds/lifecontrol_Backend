from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.item import ItemType


class ItemCreate(BaseModel):
    name: str
    type: ItemType = ItemType.other
    description: Optional[str] = None
    purchase_value: Optional[float] = None
    current_value: Optional[float] = None
    purchase_date: Optional[datetime] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    plate: Optional[str] = None
    mileage: Optional[float] = None
    specs: Dict[str, Any] = {}
    tags: List[str] = []


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    current_value: Optional[float] = None
    mileage: Optional[float] = None
    specs: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None
