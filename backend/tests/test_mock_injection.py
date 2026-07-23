import pytest
from uuid import uuid4
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from src.sale.models import Sale, SaleItem
from src.shared.interfaces import SaleRepositoryProtocol, InventoryRepositoryProtocol
from src.sale.service import SaleService

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


class MockPartyRepository:
    def get_party(self, party_id):
        return None

    def update_balance(self, party_id, amount):
        pass


class MockLedgerService:
    def record_transaction(self, transaction_id, entries):
        pass


def test_sale_service_record_sale():
    # Arrange
    sale_repo = MockSaleRepository()
    inv_repo = MockInventoryRepository()
    party_repo = MockPartyRepository()
    ledger_svc = MockLedgerService()
    service = SaleService(sale_repo, inv_repo, party_repo, ledger_svc)

    # Setup a product in inventory
    product_id = uuid4()
    from src.inventory.models import Product
    product = Product(product_id=product_id, name="Test Prod", selling_price=Decimal("10.0"), quantity=10)
    inv_repo.add_product(product)
    
    items_data = [{"product_id": product_id, "quantity": 2}]

    # Act
    sale = service.record_sale(items_data=items_data)

    # Assert
    # 1. Check if sale was recorded
    assert len(sale_repo.list_sales()) == 1
    
    # 2. Check if inventory was decreased (10 - 2 = 8)
    updated_product = inv_repo.get_product(product_id)
    assert updated_product.quantity == 8
    
    print("\nSuccess: SaleService logic verified with Mock repositories!")
