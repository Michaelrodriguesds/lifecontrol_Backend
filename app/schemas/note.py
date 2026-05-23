from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.note import NoteType


class NoteCreate(BaseModel):
    title: str
    content: str = ""
    note_type: NoteType = NoteType.markdown
    color: Optional[str] = "#1e293b"
    tags: List[str] = []
    is_pinned: bool = False
    reminder_at: Optional[datetime] = None


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    color: Optional[str] = None
    tags: Optional[List[str]] = None
    is_pinned: Optional[bool] = None
    is_archived: Optional[bool] = None
    reminder_at: Optional[datetime] = None
