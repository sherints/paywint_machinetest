from datetime import datetime, timedelta
import calendar

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Expense
from app.routers.schemas import ExpenseCreate, ExpenseOut, TotalsResponse

router = APIRouter()


@router.post("/expenses/", response_model=ExpenseOut)
async def create_expense(payload: ExpenseCreate, db: AsyncSession = Depends(get_db)):
    new_expense = Expense(
        name=payload.name,
        amount=payload.amount,
        category=payload.category
    )
    db.add(new_expense)
    await db.commit()
    await db.refresh(new_expense)
    return new_expense


@router.get("/expenses/", response_model=list[ExpenseOut])
async def get_expenses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Expense).order_by(Expense.created_at.desc()))
    return result.scalars().all()


@router.get("/expenses/month/{year}/{month}/", response_model=list[ExpenseOut])
async def get_expenses_by_month(year: int, month: int, db: AsyncSession = Depends(get_db)):
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Invalid month")

    start_date = datetime(year, month, 1)
    last_day = calendar.monthrange(year, month)[1]
    end_date = datetime(year, month, last_day, 23, 59, 59)

    result = await db.execute(
        select(Expense).where(
            Expense.created_at >= start_date,
            Expense.created_at <= end_date
        ).order_by(Expense.created_at.desc())
    )
    return result.scalars().all()


@router.get("/expenses/day/{year}/{month}/{day}/", response_model=list[ExpenseOut])
async def get_expenses_by_day(year: int, month: int, day: int, db: AsyncSession = Depends(get_db)):
    start_date = datetime(year, month, day)
    end_date = start_date + timedelta(days=1)

    result = await db.execute(
        select(Expense).where(
            Expense.created_at >= start_date,
            Expense.created_at < end_date
        ).order_by(Expense.created_at.desc())
    )
    return result.scalars().all()


@router.get("/expenses/week/{year}/{week}/", response_model=list[ExpenseOut])
async def get_expenses_by_week(year: int, week: int, db: AsyncSession = Depends(get_db)):
    start_date = datetime.fromisocalendar(year, week, 1)
    end_date = start_date + timedelta(days=7)

    result = await db.execute(
        select(Expense).where(
            Expense.created_at >= start_date,
            Expense.created_at < end_date
        ).order_by(Expense.created_at.desc())
    )
    return result.scalars().all()


@router.get("/expenses/category/{category}/", response_model=list[ExpenseOut])
async def get_expenses_by_category(category: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Expense).where(
            func.lower(Expense.category) == category.lower()
        ).order_by(Expense.created_at.desc())
    )
    return result.scalars().all()


@router.get("/totals/", response_model=TotalsResponse)
async def get_totals(
    total_salary: float = Query(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(func.coalesce(func.sum(Expense.amount), 0.0)))
    total_expense = float(result.scalar() or 0.0)
    remaining_amount = total_salary - total_expense

    return TotalsResponse(
        total_expense=round(total_expense, 2),
        total_salary=round(total_salary, 2),
        remaining_amount=round(remaining_amount, 2)
    )