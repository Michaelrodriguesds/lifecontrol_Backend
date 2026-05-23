from fastapi import APIRouter, Depends, HTTPException, Query
from app.auth.dependencies import get_current_user
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/api/expenses", tags=["expenses"])


@router.get("/")
async def list_expenses(
    month: Optional[int] = None,
    year: Optional[int] = None,
    category_id: Optional[str] = None,
    limit: int = Query(default=50, le=200),
    user=Depends(get_current_user)
):
    query = Expense.find(Expense.user_id == user["id"])
    expenses = await query.sort(-Expense.date).limit(limit).to_list()
    result = []
    for e in expenses:
        if month and e.date.month != month:
            continue
        if year and e.date.year != year:
            continue
        d = e.dict()
        d["id"] = str(e.id)
        result.append(d)
    return result


@router.post("/", status_code=201)
async def create_expense(data: ExpenseCreate, user=Depends(get_current_user)):
    expense = Expense(user_id=user["id"], **{**data.dict(), "date": data.date or datetime.utcnow()})
    await expense.insert()
    d = expense.dict()
    d["id"] = str(expense.id)
    return d


@router.put("/{expense_id}")
async def update_expense(expense_id: str, data: ExpenseUpdate, user=Depends(get_current_user)):
    expense = await Expense.get(expense_id)
    if not expense or expense.user_id != user["id"]:
        raise HTTPException(status_code=404, detail="Gasto não encontrado")
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    await expense.update({"$set": update_data})
    await expense.sync()
    d = expense.dict()
    d["id"] = str(expense.id)
    return d


@router.delete("/{expense_id}", status_code=204)
async def delete_expense(expense_id: str, user=Depends(get_current_user)):
    expense = await Expense.get(expense_id)
    if not expense or expense.user_id != user["id"]:
        raise HTTPException(status_code=404, detail="Gasto não encontrado")
    await expense.delete()


@router.get("/summary/monthly")
async def monthly_summary(year: int = datetime.utcnow().year, user=Depends(get_current_user)):
    expenses = await Expense.find(Expense.user_id == user["id"]).to_list()
    monthly = {}
    for e in expenses:
        if e.date.year == year:
            key = e.date.month
            monthly[key] = monthly.get(key, 0) + e.amount
    return {"year": year, "monthly": monthly}
