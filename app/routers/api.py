from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.routers import schemas
from app.routers.schemas import ExpenseCreate
from .. import models
from ..database import get_db


router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.post("/expenses")
async def create_expense(
   expense:ExpenseCreate,
     db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(models.Expense))
    expenses   = result.scalars().all()
    new_expense = models.Expense(
        key_name=key.key_name,
       
    )
    db.add(new_expense)
    await db.commit()
    await db.refresh(new_expense)
    return schemas.ExpenseOut(
        id=new_expense.id,
        name=new_expense.name,
        category=new_expense.category,
        amount=new_expense.amount,
        date=new_expense.created_at
    )
