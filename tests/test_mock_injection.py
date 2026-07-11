import pytest
from uuid import uuid4
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sale.models import Sale, SaleItem
from shared.interfaces import SaleRepositoryProtocol

# This is a "Fake" repository. 
# It follows the SaleRepositoryProtocol contract but doesn't touch the disk.
class MockSaleRepository(SaleRepositoryProtocol):
    def __init__(self):
        self._sales = {}

    def add_sale(self, sale: Sale) -> None:
        self._sales[sale.sale_id] = sale

    def list_sales(self) -> List[Sale]:
        return list(self._sales.values())

    def get_sale(self, sale_id: UUID) -> Optional[Sale]:
        return self._sales.get(sale_id)

def test_service_with_mock_repo():
    # Arrange
    # We inject the Mock instead of the real JSON repository
    mock_repo = MockSaleRepository()
    
    sale_id = uuid4()
    sale = Sale(
        sale_id=sale_id, 
        date=datetime.now(), 
        items=[SaleItem(uuid4(), "Mock Product", 10.0, 1)], 
        customer_name="Mock Customer"
    )

    # Act
    mock_repo.add_sale(sale)
    result = mock_repo.get_sale(sale_id)

    # Assert
    assert result == sale
    print("\nSuccess: The service layer works with a Mock repository!")
