from src.inventory.models import Product
from src.shared.interfaces import InventoryRepositoryProtocol
from src.shared.exceptions import ProductNotFoundError, InvalidProductDataError
import uuid
from decimal import Decimal

class InventoryService:
    def __init__(self, repository: InventoryRepositoryProtocol):
        self.repository = repository

    def list_products(self, show_archived: bool = False) -> list[Product]:
        products = self.repository.list_products()
        if not show_archived:
            products = [p for p in products if not p.archived]
        return products

    def add_product(self, name: str, selling_price: Decimal, quantity: int, gst_rate: Decimal = Decimal("0"), hsn_code: str = "") -> Product:
        price = selling_price
        rate = gst_rate
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

    def update_product(self, product_id: uuid.UUID, data) -> Product:
        existing = self.get_product(product_id)
        updated = Product(
            product_id=product_id,
            name=data.name if data.name is not None else existing.name,
            selling_price=data.selling_price if data.selling_price is not None else existing.selling_price,
            quantity=data.quantity if data.quantity is not None else existing.quantity,
            gst_rate=data.gst_rate if data.gst_rate is not None else existing.gst_rate,
            hsn_code=data.hsn_code if data.hsn_code is not None else existing.hsn_code,
            archived=data.archived if data.archived is not None else existing.archived,
        )
        self.repository.update_product(updated)
        return self.repository.get_product(product_id)

    def search_products(self, query: str) -> list[Product]:
        return self.repository.search_products(query)

    def delete_product(self, product_id: uuid.UUID) -> bool:
        return self.repository.delete_product(product_id)
