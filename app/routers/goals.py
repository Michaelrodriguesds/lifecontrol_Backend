from fastapi import APIRouter, Depends, HTTPException
from app.auth.dependencies import get_current_user
from app.models.goal import Goal, GoalTransaction
from app.schemas.goal import GoalCreate, GoalUpdate, TransactionCreate
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/api/goals", tags=["goals"])


@router.get("/")
async def list_goals(user=Depends(get_current_user)):
    goals = await Goal.find(Goal.user_id == user["id"]).to_list()
    result = []
    for g in goals:
        d = g.dict()
        d["id"] = str(g.id)
        d["progress_percentage"] = g.progress_percentage
        result.append(d)
    return result


@router.post("/", status_code=201)
async def create_goal(data: GoalCreate, user=Depends(get_current_user)):
    goal = Goal(user_id=user["id"], **data.dict())
    await goal.insert()
    d = goal.dict()
    d["id"] = str(goal.id)
    d["progress_percentage"] = goal.progress_percentage
    return d


@router.get("/{goal_id}")
async def get_goal(goal_id: str, user=Depends(get_current_user)):
    goal = await Goal.get(goal_id)
    if not goal or goal.user_id != user["id"]:
        raise HTTPException(status_code=404, detail="Meta não encontrada")
    d = goal.dict()
    d["id"] = str(goal.id)
    d["progress_percentage"] = goal.progress_percentage
    # Buscar transações
    transactions = await GoalTransaction.find(
        GoalTransaction.goal_id == goal_id
    ).sort(-GoalTransaction.date).to_list()
    d["transactions"] = [{"id": str(t.id), **{k: v for k, v in t.dict().items() if k != "id"}} for t in transactions]
    return d


@router.put("/{goal_id}")
async def update_goal(goal_id: str, data: GoalUpdate, user=Depends(get_current_user)):
    goal = await Goal.get(goal_id)
    if not goal or goal.user_id != user["id"]:
        raise HTTPException(status_code=404, detail="Meta não encontrada")
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    await goal.update({"$set": update_data})
    await goal.sync()
    d = goal.dict()
    d["id"] = str(goal.id)
    d["progress_percentage"] = goal.progress_percentage
    return d


@router.delete("/{goal_id}", status_code=204)
async def delete_goal(goal_id: str, user=Depends(get_current_user)):
    goal = await Goal.get(goal_id)
    if not goal or goal.user_id != user["id"]:
        raise HTTPException(status_code=404, detail="Meta não encontrada")
    await goal.delete()
    await GoalTransaction.find(GoalTransaction.goal_id == goal_id).delete()


@router.post("/{goal_id}/transactions", status_code=201)
async def add_transaction(goal_id: str, data: TransactionCreate, user=Depends(get_current_user)):
    goal = await Goal.get(goal_id)
    if not goal or goal.user_id != user["id"]:
        raise HTTPException(status_code=404, detail="Meta não encontrada")
    tx = GoalTransaction(
        goal_id=goal_id,
        user_id=user["id"],
        amount=data.amount,
        description=data.description,
        transaction_type=data.transaction_type,
        date=data.date or datetime.utcnow(),
    )
    await tx.insert()
    # Atualizar saldo da meta
    if data.transaction_type == "deposit":
        goal.current_amount += data.amount
    else:
        goal.current_amount = max(goal.current_amount - data.amount, 0)
    goal.updated_at = datetime.utcnow()
    await goal.save()
    return {"id": str(tx.id), **tx.dict()}
