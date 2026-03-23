from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.config import settings
from app.database import engine, Base
from app.routers.api import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router)


@app.get("/")
async def root():
    return {
        "message": "Expense Management API is running",
        "docs": "/docs"
    }