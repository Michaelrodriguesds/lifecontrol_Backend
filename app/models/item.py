from beanie import Document
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ItemType(str, Enum):
    vehicle = "vehicle"
    motorcycle = "motorcycle"
    computer = "computer"
    project = "project"
    service = "service"
    appliance = "appliance"
    other = "other"


class Item(Document):
    user_id: str
    name: str
    type: ItemType = ItemType.other
    description: Optional[str] = None
    purchase_value: Optional[float] = None
    current_value: Optional[float] = None
    purchase_date: Optional[datetime] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    plate: Optional[str] = None      # Para veículos
    mileage: Optional[float] = None  # Para veículos
    specs: Dict[str, Any] = {}       # Specs customizadas
    tags: List[str] = []
    image_url: Optional[str] = None
    is_active: bool = True
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Settings:
        name = "items"
