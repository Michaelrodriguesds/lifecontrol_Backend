from fastapi import APIRouter, Depends, HTTPException
from app.auth.dependencies import get_current_user
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate
from datetime import datetime

router = APIRouter(prefix="/api/items", tags=["items"])


@router.get("/")
async def list_items(user=Depends(get_current_user)):
    items = await Item.find(Item.user_id == user["id"], Item.is_active == True).to_list()
    return [{"id": str(i.id), **{k: v for k, v in i.dict().items() if k != "id"}} for i in items]


@router.post("/", status_code=201)
async def create_item(data: ItemCreate, user=Depends(get_current_user)):
    item = Item(user_id=user["id"], **data.dict())
    await item.insert()
    d = item.dict()
    d["id"] = str(item.id)
    return d


@router.get("/{item_id}")
async def get_item(item_id: str, user=Depends(get_current_user)):
    item = await Item.get(item_id)
    if not item or item.user_id != user["id"]:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    d = item.dict()
    d["id"] = str(item.id)
    return d


@router.put("/{item_id}")
async def update_item(item_id: str, data: ItemUpdate, user=Depends(get_current_user)):
    item = await Item.get(item_id)
    if not item or item.user_id != user["id"]:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    await item.update({"$set": update_data})
    await item.sync()
    d = item.dict()
    d["id"] = str(item.id)
    return d


@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: str, user=Depends(get_current_user)):
    item = await Item.get(item_id)
    if not item or item.user_id != user["id"]:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    await item.update({"$set": {"is_active": False}})
