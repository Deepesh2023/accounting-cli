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

def test_list_sales(sale_repo):
    # Arrange
    sales_to_add = [
        Sale(sale_id=uuid4(), date=datetime.now(), items=[SaleItem(uuid4(), "P1", 10.0, 1)], customer_name="C1"),
        Sale(sale_id=uuid4(), date=datetime.now(), items=[SaleItem(uuid4(), "P2", 20.0, 2)], customer_name="C2"),
    ]
    for s in sales_to_add:
        sale_repo.add_sale(s)

    # Act
    sales = sale_repo.list_sales()

    # Assert
    assert len(sales) == 2
    assert sales == sales_to_add

def test_persistence(sale_repo):
    # Arrange
    sale_id = uuid4()
    item = SaleItem(product_id=uuid4(), name="Persistent Product", selling_price=15.0, quantity=1)
    sale = Sale(sale_id=sale_id, date=datetime.now(), items=[item], customer_name="Jane Doe")
    sale_repo.add_sale(sale)

    # Act
    # Create a new repository instance pointing to the same file to test loading
    new_repo = SaleRepository(storage_file=TEST_STORAGE)
    retrieved_sale = new_repo.get_sale(sale_id)

    # Assert
    assert retrieved_sale is not None
    assert retrieved_sale == sale



