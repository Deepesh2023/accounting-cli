import pytest
import os
from uuid import uuid4
from datetime import datetime
from sale.models import Sale, SaleItem
from sale.repository import SaleRepository

TEST_STORAGE = "test_sales.json"

@pytest.fixture
def sale_repo():
    # Cleanup before and after test
    if os.path.exists(TEST_STORAGE):
        os.remove(TEST_STORAGE)
    repo = SaleRepository(storage_file=TEST_STORAGE)
    yield repo
    if os.path.exists(TEST_STORAGE):
        os.remove(TEST_STORAGE)

def test_add_sale(sale_repo):
    # Arrange
    sale_id = uuid4()
    item = SaleItem(product_id=uuid4(), name="Test Product", selling_price=10.0, quantity=2)
    sale = Sale(sale_id=sale_id, date=datetime.now(), items=[item], customer_name="John Doe")

    # Act
    sale_repo.add_sale(sale)
    
    # Assert
    sales = sale_repo.list_sales()
    assert len(sales) == 1
    assert sales[0].sale_id == sale_id
    assert sales[0].customer_name == "John Doe"
    assert len(sales[0].items) == 1
    assert sales[0].items[0].name == "Test Product"

def test_get_sale(sale_repo):
    # Arrange
    sale_id = uuid4()
    item = SaleItem(product_id=uuid4(), name="Test Product", selling_price=10.0, quantity=2)
    sale = Sale(sale_id=sale_id, date=datetime.now(), items=[item], customer_name="John Doe")
    sale_repo.add_sale(sale)

    # Act
    retrieved_sale = sale_repo.get_sale(sale_id)
    non_existent_sale = sale_repo.get_sale(uuid4())

    # Assert
    assert retrieved_sale == sale
    assert non_existent_sale is None

