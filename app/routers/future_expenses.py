from fastapi import APIRouter, Depends, HTTPException
from app.auth.dependencies import get_current_user
from app.models.future_expense import FutureExpense
from app.schemas.future_expense import FutureExpenseCreate, FutureExpenseUpdate
from datetime import datetime

router = APIRouter(prefix="/api/future-expenses", tags=["future_expenses"])


@router.get("/")
async def list_future_expenses(user=Depends(get_current_user)):
    items = await FutureExpense.find(FutureExpense.user_id == user["id"]).to_list()
    result = []
    for f in items:
        d = f.dict()
        d["id"] = str(f.id)
        d["remaining_amount"] = f.remaining_amount
        result.append(d)
    return result


@router.post("/", status_code=201)
async def create_future_expense(data: FutureExpenseCreate, user=Depends(get_current_user)):
    fe = FutureExpense(user_id=user["id"], **data.dict())
    await fe.insert()
    d = fe.dict()
    d["id"] = str(fe.id)
    d["remaining_amount"] = fe.remaining_amount
    return d


@router.put("/{fe_id}")
async def update_future_expense(fe_id: str, data: FutureExpenseUpdate, user=Depends(get_current_user)):
    fe = await FutureExpense.get(fe_id)
    if not fe or fe.user_id != user["id"]:
        raise HTTPException(status_code=404, detail="Não encontrado")
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    if data.is_paid:
        update_data["paid_at"] = datetime.utcnow()
    update_data["updated_at"] = datetime.utcnow()
    await fe.update({"$set": update_data})
    await fe.sync()
    d = fe.dict()
    d["id"] = str(fe.id)
    d["remaining_amount"] = fe.remaining_amount
    return d


@router.delete("/{fe_id}", status_code=204)
async def delete_future_expense(fe_id: str, user=Depends(get_current_user)):
    fe = await FutureExpense.get(fe_id)
    if not fe or fe.user_id != user["id"]:
        raise HTTPException(status_code=404, detail="Não encontrado")
    await fe.delete()
