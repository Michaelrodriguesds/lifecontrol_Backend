# app/models/work_day.py
from beanie import Document
from typing import Optional
from datetime import datetime
from pydantic import Field


class WorkDay(Document):
    """
    Registro de um dia de trabalho no Mercado Livre.

    Regras de negócio:
      - Diária bruta:  R$ 230,00
      - Combustível:   −R$ 52,00 se abasteceu (fueled=True)
      - PNR:           −valor informado pelo usuário (Pedido Não Recebido)
      - Líquido:       230 − (52 se combustível) − pnr_amount

    Pagamento:
      - Dias 1 a 15   → pago no dia 10 do mês seguinte
      - Dias 16 a 31  → pago no dia 25 do mês seguinte
    """
    user_id:    str
    date:       str            # YYYY-MM-DD — facilita filtros por mês
    worked:     bool  = False
    fueled:     bool  = False  # abasteceu → -R$ 52
    pnr_amount: float = 0.0    # valor da cobrança PNR (0 = sem ocorrência)
    notes:      Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "work_days"