from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

client: AsyncIOMotorClient = None


async def connect_to_mongo():
    global client
    try:
        client = AsyncIOMotorClient(
            settings.MONGO_URL,
            serverSelectionTimeoutMS=5000
        )
        # Importar todos os modelos Beanie
        from app.models.user import User
        from app.models.goal import Goal, GoalTransaction
        from app.models.item import Item
        from app.models.expense import Expense
        from app.models.future_expense import FutureExpense
        from app.models.note import Note
        from app.models.category import Category
        from app.models.work_day import WorkDay   # ← novo modelo

        await init_beanie(
            database=client[settings.DATABASE_NAME],
            document_models=[
                User, Goal, GoalTransaction,
                Item, Expense, FutureExpense,
                Note, Category,
                WorkDay,   # ← registrar no Beanie
            ]
        )
        logger.info(f"✅ Conectado ao MongoDB: {settings.DATABASE_NAME}")
    except Exception as e:
        logger.error(f"❌ Erro ao conectar MongoDB: {e}")
        raise


async def close_mongo_connection():
    global client
    if client:
        client.close()
        logger.info("MongoDB desconectado")
