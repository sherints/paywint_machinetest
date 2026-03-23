from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class ExpenseCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=50)


class ExpenseOut(BaseModel):
    id: int
    name: str
    amount: float
    category: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TotalsResponse(BaseModel):
    total_expense: float
    total_salary: float
    remaining_amount: float