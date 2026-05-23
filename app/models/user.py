from beanie import Document, Indexed
from pydantic import EmailStr
from typing import Optional
from datetime import datetime


class User(Document):
    name: str
    email: Indexed(EmailStr, unique=True)
    hashed_password: str
    is_active: bool = True
    avatar: Optional[str] = None
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Settings:
        name = "users"
        indexes = ["email"]
