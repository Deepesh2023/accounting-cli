from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

from inventory.models import Product
from parties.models import Party

class Sale(SQLModel, table=True):
    sale_id: UUID = Field(primary_key=True)
    date: datetime = Field(default_factory=datetime.now)
    
    # Link to Party (Customer)
    party_id: Optional[UUID] = Field(default=None, foreign_key="parties.party_id")
    
    # Financial Totals
    total_taxable: Decimal = Field(default=0, nullable=False)
    total_tax: Decimal = Field(default=0, nullable=False)
    grand_total: Decimal = Field(default=0, nullable=False)
    paid_amount: Decimal = Field(default=0, nullable=False)
    balance_amount: Decimal = Field(default=0, nullable=False)
    
    # Settings
    round_off: bool = Field(default=False)
    
    # Relationships
    items: List["SaleItem"] = Relationship(back_populates="sale")
    party: Optional[Party] = Relationship()

class SaleItem(SQLModel, table=True):
    sale_item_id: UUID = Field(primary_key=True)
    sale_id: UUID = Field(foreign_key="sale.sale_id")
    
    # Product Link
    product_id: UUID = Field(foreign_key="products.product_id")
    
    # Row Level Data
    name: str = Field(nullable=False) # Snapshot of name at time of sale
    quantity: int = Field(nullable=False)
    price: Decimal = Field(nullable=False)
    discount_amount: Decimal = Field(default=0, nullable=False)
    taxable_amount: Decimal = Field(default=0, nullable=False)
    tax_amount: Decimal = Field(default=0, nullable=False)
    row_total: Decimal = Field(default=0, nullable=False)
    
    # Relationships
    sale: Sale = Relationship(back_populates="items")
    product: Product = Relationship()
