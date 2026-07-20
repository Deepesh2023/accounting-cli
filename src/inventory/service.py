from inventory.models import Product
from shared.interfaces import InventoryRepositoryProtocol
from shared.exceptions import ProductNotFoundError, InvalidProductDataError
import uuid
from decimal import Decimal

class InventoryService:
    def __init__(self, repository: InventoryRepositoryProtocol):
        self.repository = repository

    def list_products(self, show_archived: bool = False) -> list[Product]:
        return [
            p for p in self.repository.list_products() 
            if p.archived == show_archived
        ]

    def add_product(self, name: str, selling_price: float | Decimal, quantity: int, gst_rate: float | Decimal = 0, hsn_code: str = "") -> Product:
        price = Decimal(str(selling_price))
        rate = Decimal(str(gst_rate))
        if price < 0 or quantity < 0 or rate < 0:
            raise InvalidProductDataError("selling-price/quantity/gst-rate shouldn't be negative")
        
        product = Product(
            product_id=uuid.uuid4(),
            name=name,
            selling_price=price,
            gst_rate=rate,
            hsn_code=hsn_code,
            quantity=quantity,
        )
        self.repository.add_product(product)
        return product

    def change_visibility(self, product_id: uuid.UUID) -> Product:
        result = self.repository.change_visibility(product_id)
        if not result:
            raise ProductNotFoundError("Product not found.")
        return result

    def get_product(self, product_id: uuid.UUID) -> Product:
        product = self.repository.get_product(product_id)
        if not product:
            raise ProductNotFoundError("Product not found.")
        return product

    def update_product(self, product: Product) -> None:
        self.repository.update_product(product)

    def search_products(self, query: str) -> list[Product]:
        return self.repository.search_products(query)
