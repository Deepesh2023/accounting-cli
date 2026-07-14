from uuid import UUID
from decimal import Decimal
from sqlalchemy_orm import Mapped, mapped_column
from src.storage.database import Base

class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    selling_price: Mapped[Decimal] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    archived: Mapped[bool] = mapped_column(default=False)

