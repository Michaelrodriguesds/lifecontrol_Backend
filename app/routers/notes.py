from fastapi import APIRouter, Depends, HTTPException
from app.auth.dependencies import get_current_user
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate
from datetime import datetime

router = APIRouter(prefix="/api/notes", tags=["notes"])


@router.get("/")
async def list_notes(user=Depends(get_current_user)):
    notes = await Note.find(
        Note.user_id == user["id"],
        Note.is_archived == False
    ).sort(-Note.is_pinned, -Note.updated_at).to_list()
    return [{"id": str(n.id), **{k: v for k, v in n.dict().items() if k != "id"}} for n in notes]


@router.post("/", status_code=201)
async def create_note(data: NoteCreate, user=Depends(get_current_user)):
    note = Note(user_id=user["id"], **data.dict())
    await note.insert()
    d = note.dict()
    d["id"] = str(note.id)
    return d


@router.put("/{note_id}")
async def update_note(note_id: str, data: NoteUpdate, user=Depends(get_current_user)):
    note = await Note.get(note_id)
    if not note or note.user_id != user["id"]:
        raise HTTPException(status_code=404, detail="Nota não encontrada")
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    await note.update({"$set": update_data})
    await note.sync()
    d = note.dict()
    d["id"] = str(note.id)
    return d


@router.delete("/{note_id}", status_code=204)
async def delete_note(note_id: str, user=Depends(get_current_user)):
    note = await Note.get(note_id)
    if not note or note.user_id != user["id"]:
        raise HTTPException(status_code=404, detail="Nota não encontrada")
    await note.delete()
