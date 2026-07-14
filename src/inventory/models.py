from uuid import UUID
from decimal import Decimal
from sqlmodel import SQLModel, Field

class Product(SQLModel, table=True):
    product_id: UUID = Field(primary_key=True)
    name: str = Field(nullable=False)
    selling_price: Decimal = Field(nullable=False)
    quantity: int = Field(nullable=False)
    archived: bool = Field(default=False)

