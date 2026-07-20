from uuid import UUID, uuid4
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlmodel import SQLModel, Field

class Expense(SQLModel, table=True, __tablename__="expense"):
    expense_id: UUID = Field(default_factory=uuid4, primary_key=True)
    date: datetime = Field(default_factory=datetime.now)
    category: str = Field(nullable=False)
    paid_by: str = Field(nullable=False) # e.g., "Cash", "Bank", or a specific Party
    amount: Decimal = Field(nullable=False)
    notes: Optional[str] = Field(default=None)
