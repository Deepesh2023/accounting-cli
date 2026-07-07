from dataclasses import dataclass
from uuid import UUID


@dataclass
class Product:
    product_id: UUID
    name: str
    selling_price: float
    quantity: int
    archived: bool = False
