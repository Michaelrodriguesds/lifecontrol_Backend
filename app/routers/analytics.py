from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user
from app.models.expense import Expense
from app.models.goal import Goal, GoalStatus
from app.models.item import Item
from app.models.future_expense import FutureExpense
from datetime import datetime
from collections import defaultdict

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

# Nomes curtos dos meses em pt-BR para o gráfico
MONTHS_PT = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']


@router.get("/dashboard")
async def dashboard_summary(user=Depends(get_current_user)):
    uid = user["id"]
    now = datetime.utcnow()

    # ─── Buscar dados do usuário no banco ────────────────────────────────────
    expenses       = await Expense.find(Expense.user_id == uid).to_list()
    goals          = await Goal.find(Goal.user_id == uid).to_list()
    future_exp     = await FutureExpense.find(FutureExpense.user_id == uid).to_list()

    # Item é opcional — só busca se o modelo existir
    try:
        items = await Item.find(Item.user_id == uid).to_list()
    except Exception:
        items = []

    # ─── Metas ───────────────────────────────────────────────────────────────
    # total_invested = soma do valor já guardado em cada meta
    total_invested = sum(getattr(g, 'current_amount', 0) or 0 for g in goals)
    goals_active    = sum(1 for g in goals if g.status == GoalStatus.active)
    goals_completed = sum(1 for g in goals if g.status == GoalStatus.completed)

    # ─── Gastos ──────────────────────────────────────────────────────────────
    # Gastos do mês atual
    monthly_spent = sum(
        e.amount for e in expenses
        if e.date.month == now.month and e.date.year == now.year
    )

    # Gastos futuros não pagos e em atraso
    unpaid_future  = [f for f in future_exp if not getattr(f, 'is_paid', False)]
    pending_total  = sum(getattr(f, 'predicted_amount', 0) or 0 for f in unpaid_future)
    overdue_count  = sum(
        1 for f in unpaid_future
        if getattr(f, 'due_date', None) and f.due_date < now
    )

    # ─── Itens ───────────────────────────────────────────────────────────────
    items_count      = len(items)
    items_total_value = sum(getattr(i, 'value', 0) or 0 for i in items)

    # ─── Gráfico: gastos mensais (últimos 12 meses) ──────────────────────────
    # Agrupa os gastos por ano-mês e formata para o gráfico de barras
    by_month: dict = defaultdict(float)
    for e in expenses:
        key = (e.date.year, e.date.month)
        by_month[key] += e.amount

    monthly_expenses_chart = []
    for i in range(11, -1, -1):
        # Calcula qual mês é esse (contando para trás a partir de hoje)
        month_num = ((now.month - 1 - i) % 12) + 1
        year_num  = now.year + ((now.month - 1 - i) // 12)
        monthly_expenses_chart.append({
            "month": MONTHS_PT[month_num - 1],
            "total": by_month.get((year_num, month_num), 0.0),
        })

    # ─── Gráfico: top categorias ─────────────────────────────────────────────
    by_category: dict = defaultdict(float)
    for e in expenses:
        cat = getattr(e, 'category_name', None) or "Sem categoria"
        by_category[cat] += e.amount

    top_categories = sorted(
        [{"category": k, "total": v} for k, v in by_category.items()],
        key=lambda x: x["total"],
        reverse=True,
    )[:5]

    # ─── Resposta no formato que o dashboard.component.ts espera ─────────────
    # IMPORTANTE: o frontend acessa d().goals.total_invested, d().expenses.monthly etc.
    # Por isso a resposta precisa ser aninhada, não plana.
    return {
        "goals": {
            "total": len(goals),
            "active": goals_active,
            "completed": goals_completed,
            "total_invested": total_invested,
            "total_target": sum(getattr(g, 'target_amount', 0) or 0 for g in goals),
        },
        "expenses": {
            "monthly": monthly_spent,
            "all_time": sum(e.amount for e in expenses),
            "pending_future": pending_total,
            "overdue_count": overdue_count,
        },
        "items": {
            "count": items_count,
            "total_value": items_total_value,
        },
        "charts": {
            "monthly_expenses": monthly_expenses_chart,
            "top_categories": top_categories,
        },
    }