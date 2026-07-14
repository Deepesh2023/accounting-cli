from uuid import UUID
from datetime import datetime
from decimal import Decimal
from sqlmodel import SQLModel, Field

class LedgerEntry(SQLModel, table=True):
    entry_id: UUID = Field(primary_key=True)
    date: datetime = Field(default_factory=datetime.now)
    
    # The account being hit (e.g., "Cash", "Sales", "Customer: John Doe")
    account_name: str = Field(nullable=False)
    
    # Double Entry values
    debit: Decimal = Field(default=0, nullable=False)
    credit: Decimal = Field(default=0, nullable=False)
    
    # Reference to the source transaction (Sale or Purchase ID)
    transaction_id: UUID = Field(nullable=False)
    description: str = Field(nullable=True)
