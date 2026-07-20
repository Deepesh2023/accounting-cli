from uuid import UUID
from decimal import Decimal
from sqlmodel import SQLModel, Field
import enum

class PartyType(enum.Enum):
    DEBTOR = "DEBTOR"     # Customer (Asset)
    CREDITOR = "CREDITOR" # Supplier (Liability)

class Party(SQLModel, table=True, __tablename__="parties"):
    party_id: UUID = Field(primary_key=True)
    name: str = Field(nullable=False)
    party_type: PartyType = Field(nullable=False)
    balance: Decimal = Field(default=0, nullable=False)
    address: str | None = Field(default=None)
    phone: str | None = Field(default=None)
    state: str = Field(default="", nullable=False)
    gstin: str | None = Field(default=None)
