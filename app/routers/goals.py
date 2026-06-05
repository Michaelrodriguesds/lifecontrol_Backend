# app/routers/goals.py
from fastapi import APIRouter, Depends, HTTPException
from app.auth.dependencies import get_current_user
from app.models.goal import Goal, GoalTransaction
from app.schemas.goal import GoalCreate, GoalUpdate, TransactionCreate
from datetime import datetime

router = APIRouter(prefix="/api/goals", tags=["goals"])


def _serialize(g: Goal) -> dict:
    d = g.model_dump()
    d["id"]                 = str(g.id)
    d["progress_percent"]   = g.progress_percentage          # nome que o frontend usa
    d["progress_percentage"]= g.progress_percentage
    d["remaining_amount"]   = max(g.target_amount - g.current_amount, 0)
    return d


@router.get("/")
async def list_goals(user=Depends(get_current_user)):
    goals = await Goal.find(Goal.user_id == user["id"]).to_list()
    return [_serialize(g) for g in goals]


@router.post("/", status_code=201)
async def create_goal(data: GoalCreate, user=Depends(get_current_user)):
    goal = Goal(user_id=user["id"], **data.model_dump())
    await goal.insert()
    return _serialize(goal)


@router.get("/{goal_id}")
async def get_goal(goal_id: str, user=Depends(get_current_user)):
    goal = await Goal.get(goal_id)
    if not goal or goal.user_id != user["id"]:
        raise HTTPException(status_code=404, detail="Meta não encontrada")
    d = _serialize(goal)
    txs = await GoalTransaction.find(
        GoalTransaction.goal_id == goal_id
    ).sort(-GoalTransaction.date).to_list()
    d["transactions"] = [
        {"id": str(t.id), **{k: v for k, v in t.model_dump().items() if k != "id"}}
        for t in txs
    ]
    return d


@router.put("/{goal_id}")
async def update_goal(goal_id: str, data: GoalUpdate, user=Depends(get_current_user)):
    goal = await Goal.get(goal_id)
    if not goal or goal.user_id != user["id"]:
        raise HTTPException(status_code=404, detail="Meta não encontrada")
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    await goal.update({"$set": update_data})
    await goal.sync()
    return _serialize(goal)


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

    # Atualizar saldo
    if data.transaction_type == "deposit":
        goal.current_amount += data.amount
    else:
        goal.current_amount = max(goal.current_amount - data.amount, 0)

    # Marcar como concluída se atingiu a meta
    if goal.current_amount >= goal.target_amount:
        goal.status = "completed"

    goal.updated_at = datetime.utcnow()
    await goal.save()
    return {"id": str(tx.id), **tx.model_dump()}