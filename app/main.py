from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.routers import auth, goals, expenses, items, future_expenses, notes, analytics
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="API LifeControl — Gerenciamento de vida financeira",
    lifespan=lifespan,
)

# CORS — permitir frontend Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(auth.router)
app.include_router(goals.router)
app.include_router(expenses.router)
app.include_router(items.router)
app.include_router(future_expenses.router)
app.include_router(notes.router)
app.include_router(analytics.router)


@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "dev_mode": settings.DEV_MODE,
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    return {"status": "ok", "dev_mode": settings.DEV_MODE}
