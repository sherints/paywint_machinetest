import datetime

from pydantic import BaseModel
from typing import List, Dict

class ExpenseCreate(BaseModel):
    
    name: str
    category: str
    amount: int

class ExpenseOut (ExpenseCreate):
    id:int
    date:datetime