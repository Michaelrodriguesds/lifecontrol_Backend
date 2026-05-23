from beanie import Document
from typing import Optional, List
from datetime import datetime
from enum import Enum


class NoteType(str, Enum):
    free = "free"
    checklist = "checklist"
    markdown = "markdown"


class Note(Document):
    user_id: str
    title: str
    content: str = ""
    note_type: NoteType = NoteType.markdown
    color: Optional[str] = "#1e293b"
    tags: List[str] = []
    is_pinned: bool = False
    reminder_at: Optional[datetime] = None
    is_archived: bool = False
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Settings:
        name = "notes"
