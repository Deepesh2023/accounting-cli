from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import List, Optional

@dataclass
class SaleItem:
    product_id: UUID
    name: str
    selling_price: float
    quantity: int

@dataclass
class Sale:
    sale_id: UUID
    date: datetime
    items: List[SaleItem]
    customer_name: Optional[str] = None
