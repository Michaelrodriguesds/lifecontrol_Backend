from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user
from app.models.expense import Expense
from app.models.goal import Goal, GoalStatus
from app.models.future_expense import FutureExpense
from datetime import datetime
from collections import defaultdict

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/dashboard")
async def dashboard_summary(user=Depends(get_current_user)):
    uid = user["id"]
    now = datetime.utcnow()

    expenses = await Expense.find(Expense.user_id == uid).to_list()
    goals = await Goal.find(Goal.user_id == uid).to_list()
    future_expenses = await FutureExpense.find(
        FutureExpense.user_id == uid, FutureExpense.is_paid == False
    ).to_list()

    # Totais
    total_spent = sum(e.amount for e in expenses)
    total_invested = sum(g.current_amount for g in goals)
    goals_completed = sum(1 for g in goals if g.status == GoalStatus.completed)

    # Mensal atual
    monthly_spent = sum(
        e.amount for e in expenses
        if e.date.month == now.month and e.date.year == now.year
    )

    # Gastos por categoria
    by_category = defaultdict(float)
    for e in expenses:
        key = e.category_name or "Sem categoria"
        by_category[key] += e.amount

    # Evolução mensal (últimos 6 meses)
    monthly_evolution = {}
    for e in expenses:
        key = f"{e.date.year}-{e.date.month:02d}"
        monthly_evolution[key] = monthly_evolution.get(key, 0) + e.amount

    # Gastos futuros
    upcoming = sorted(
        [f for f in future_expenses if f.due_date],
        key=lambda x: x.due_date
    )[:5]

    return {
        "total_spent": total_spent,
        "total_invested": total_invested,
        "goals_completed": goals_completed,
        "goals_total": len(goals),
        "monthly_spent": monthly_spent,
        "by_category": dict(by_category),
        "monthly_evolution": monthly_evolution,
        "upcoming_expenses": [
            {
                "id": str(f.id),
                "title": f.title,
                "amount": f.predicted_amount,
                "due_date": f.due_date,
                "priority": f.priority,
            }
            for f in upcoming
        ],
    }
