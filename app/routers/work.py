# app/routers/work.py
from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user
from app.models.work_day import WorkDay
from app.schemas.work_day import WorkDayCreate
from datetime import datetime

router = APIRouter(prefix="/api/work", tags=["work"])

DAILY_RATE     = 230.0   # diária bruta
FUEL_DEDUCTION =  52.0   # desconto por abastecimento


def _net(day: WorkDay) -> float:
    """Calcula o valor líquido do dia."""
    if not day.worked:
        return 0.0
    return DAILY_RATE - (FUEL_DEDUCTION if day.fueled else 0.0) - (day.pnr_amount or 0.0)


def _serialize(day: WorkDay) -> dict:
    return {
        "id":         str(day.id),
        "date":       day.date,
        "worked":     day.worked,
        "fueled":     day.fueled,
        "pnr_amount": day.pnr_amount,
        "notes":      day.notes,
        "net_amount": _net(day),
    }


@router.get("/days")
async def list_days(month: str = None, user=Depends(get_current_user)):
    """Lista dias trabalhados. Filtro opcional: month=YYYY-MM"""
    days = await WorkDay.find(WorkDay.user_id == user["id"]).to_list()
    if month:
        days = [d for d in days if d.date.startswith(month)]
    return [_serialize(d) for d in days]


@router.post("/days", status_code=201)
async def save_day(data: WorkDayCreate, user=Depends(get_current_user)):
    """Cria ou atualiza o registro do dia (upsert por date)."""
    existing = await WorkDay.find_one(
        WorkDay.user_id == user["id"],
        WorkDay.date == data.date,
    )
    if existing:
        await existing.update({"$set": {
            **data.model_dump(),
            "updated_at": datetime.utcnow(),
        }})
        await existing.sync()
        return _serialize(existing)

    day = WorkDay(user_id=user["id"], **data.model_dump())
    await day.insert()
    return _serialize(day)


@router.delete("/days/{date}", status_code=204)
async def delete_day(date: str, user=Depends(get_current_user)):
    """Remove o registro de um dia."""
    day = await WorkDay.find_one(
        WorkDay.user_id == user["id"],
        WorkDay.date == date,
    )
    if day:
        await day.delete()


@router.get("/summary")
async def get_summary(month: str, user=Depends(get_current_user)):
    """
    Resumo financeiro do mês (format: YYYY-MM).

    Período 1 (dias 1–15)  → pagamento no dia 10 do mês seguinte
    Período 2 (dias 16–31) → pagamento no dia 25 do mês seguinte
    """
    all_days = await WorkDay.find(WorkDay.user_id == user["id"]).to_list()
    worked   = [d for d in all_days if d.date.startswith(month) and d.worked]

    year, mon = map(int, month.split("-"))
    next_mon  = mon + 1 if mon < 12 else 1
    next_year = year   if mon < 12 else year + 1

    p1 = [d for d in worked if int(d.date.split("-")[2]) <= 15]
    p2 = [d for d in worked if int(d.date.split("-")[2]) >  15]

    def _period(days: list, pay_day: int) -> dict:
        fuel_cnt  = sum(1 for d in days if d.fueled)
        pnr_total = sum(d.pnr_amount for d in days)
        net       = sum(_net(d) for d in days)
        return {
            "days_worked":    len(days),
            "gross":          len(days) * DAILY_RATE,
            "fuel_deduction": fuel_cnt * FUEL_DEDUCTION,
            "pnr_deduction":  pnr_total,
            "net":            net,
            "payment_date":   f"{pay_day:02d}/{next_mon:02d}/{next_year}",
        }

    return {
        "month":        month,
        "period1":      _period(p1, 10),
        "period2":      _period(p2, 25),
        "total_worked": len(worked),
        "total_net":    sum(_net(d) for d in worked),
    }