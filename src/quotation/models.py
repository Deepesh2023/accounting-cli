from uuid import UUID, uuid4
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

class Quotation(SQLModel, table=True, __tablename__="quotation"):
    quotation_id: UUID = Field(default_factory=uuid4, primary_key=True)
    date: datetime = Field(default_factory=datetime.now)
    party_id: Optional[UUID] = Field(default=None, foreign_key="party.party_id")
    total_amount: Decimal = Field(default=0, nullable=False)
    status: str = Field(default="Draft") # Draft, Sent, Converted, Expired
    notes: Optional[str] = Field(default=None)
    
    items: List["QuotationItem"] = Relationship(back_populates="quotation")

class QuotationItem(SQLModel, table=True, __tablename__="quotation_item"):
    item_id: UUID = Field(default_factory=uuid4, primary_key=True)
    quotation_id: UUID = Field(foreign_key="quotation.quotation_id")
    product_id: UUID = Field(foreign_key="product.product_id")
    name: str = Field(nullable=False)
    quantity: int = Field(nullable=False)
    unit_price: Decimal = Field(nullable=False)
    total_price: Decimal = Field(nullable=False)
    
    quotation: Quotation = Relationship(back_populates="items")
