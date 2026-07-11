import pytest
from uuid import uuid4
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sale.models import Sale, SaleItem
from shared.interfaces import SaleRepositoryProtocol, InventoryRepositoryProtocol
from sale.service import SaleService

# Mock for Sale Repository
class MockSaleRepository(SaleRepositoryProtocol):
    def __init__(self):
        self._sales = {}

    def add_sale(self, sale: Sale) -> None:
        self._sales[sale.sale_id] = sale

    def list_sales(self) -> List[Sale]:
        return list(self._sales.values())

    def get_sale(self, sale_id: UUID) -> Optional[Sale]:
        return self._sales.get(sale_id)

# Mock for Inventory Repository
class MockInventoryRepository(InventoryRepositoryProtocol):
    def __init__(self):
        self._products = {}

    def add_product(self, product) -> None:
        self._products[product.product_id] = product

    def list_products(self) -> List:
        return list(self._products.values())

    def get_product(self, product_id: UUID):
        return self._products.get(product_id)

    def update_product(self, product) -> None:
        self._products[product.product_id] = product

    def change_visibility(self, product_id: UUID):
        return self._products.get(product_id)

    def search_products(self, query: str):
        return list(self._products.values())

def test_sale_service_record_sale():
    # Arrange
    sale_repo = MockSaleRepository()
    inv_repo = MockInventoryRepository()
    service = SaleService(sale_repo, inv_repo)

    # Setup a product in inventory
    product_id = uuid4()
    from inventory.models import Product
    product = Product(product_id=product_id, name="Test Prod", selling_price=10.0, quantity=10)
    inv_repo.add_product(product)

    items = [SaleItem(product_id=product_id, name="Test Prod", selling_price=10.0, quantity=2)]

    # Act
    sale = service.record_sale(items=items, customer_name="John Doe")

    # Assert
    # 1. Check if sale was recorded
    assert sale.customer_name == "John Doe"
    assert len(sale_repo.list_sales()) == 1
    
    # 2. Check if inventory was decreased (10 - 2 = 8)
    updated_product = inv_repo.get_product(product_id)
    assert updated_product.quantity == 8
    
    print("\nSuccess: SaleService logic verified with Mock repositories!")
