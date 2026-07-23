from typing import Protocol, List, Optional
from uuid import UUID
from src.sale.models import Sale
from src.inventory.models import Product

class SaleRepositoryProtocol(Protocol):
    def add_sale(self, sale: Sale) -> None:
        ...

    def list_sales(self) -> List[Sale]:
        ...

    def get_sale(self, sale_id: UUID) -> Optional[Sale]:
        ...

class InventoryRepositoryProtocol(Protocol):
    def add_product(self, product: Product) -> None:
        ...

    def list_products(self) -> List[Product]:
        ...

    def get_product(self, product_id: UUID) -> Optional[Product]:
        ...

    def update_product(self, product: Product) -> None:
        ...

    def change_visibility(self, product_id: UUID) -> Optional[Product]:
        ...

    def search_products(self, query: str) -> List[Product]:
        ...

    def delete_product(self, product_id: UUID) -> bool:
        ...
