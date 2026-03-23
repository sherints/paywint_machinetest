import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,Float
from .database import Base

class Expense(Base):
    __tablename__ = "expense"
    id       = Column(Integer, primary_key=True, index=True)
    name    = Column(String,index=True)
    amount = Column(Float)
    category =Column(String)
    created_at =Column(DateTime,default=datetime.utcnow)

