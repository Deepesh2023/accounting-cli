from uuid import UUID
from decimal import Decimal
from sqlmodel import SQLModel, Field

class Product(SQLModel, table=True, __tablename__="product"):
    product_id: UUID = Field(primary_key=True)
    name: str = Field(nullable=False)
    selling_price: Decimal = Field(nullable=False)
    gst_rate: Decimal = Field(default=Decimal("0.0"), nullable=False)
    hsn_code: str = Field(default="", nullable=False)
    quantity: int = Field(nullable=False)
    archived: bool = Field(default=False)

