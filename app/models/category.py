from beanie import Document
from typing import Optional
from datetime import datetime


class Category(Document):
    user_id: str
    name: str
    icon: Optional[str] = None
    color: Optional[str] = "#6366f1"
    description: Optional[str] = None
    is_default: bool = False
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "categories"
