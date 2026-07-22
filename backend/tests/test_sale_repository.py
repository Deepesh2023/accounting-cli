import pytest
import os
from uuid import uuid4
from datetime import datetime
from sale.models import Sale, SaleItem
from sale.repository import SaleRepository

TEST_STORAGE = "test_sales.json"

@pytest.fixture
def sale_repo(session):
    return SaleRepository(session)

def test_add_sale(sale_repo):
    # Arrange
    sale_id = uuid4()
    item_id = uuid4()
    item = SaleItem(
        sale_item_id=item_id,
        product_id=uuid4(),
        name="Test Product",
        selling_price=10.0,
        quantity=2,
        price=10.0
    )
    sale = Sale(sale_id=sale_id, date=datetime.now(), items=[item])
    
    # Act
    sale_repo.add_sale(sale)
    
    # Assert
    sales = sale_repo.list_sales()
    assert len(sales) >= 1
    assert any(s.sale_id == sale_id for s in sales)
    sale_retrieved = next(s for s in sales if s.sale_id == sale_id)
    assert len(sale_retrieved.items) == 1
    assert sale_retrieved.items[0].name == "Test Product"


def test_get_sale(sale_repo):
    # Arrange
    sale_id = uuid4()
    item_id = uuid4()
    item = SaleItem(
        sale_item_id=item_id,
        product_id=uuid4(), 
        name="Test Product", 
        selling_price=10.0, 
        quantity=2,
        price=10.0
    )
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
        Sale(
            sale_id=uuid4(),
            date=datetime.now(),
            items=[SaleItem(sale_item_id=uuid4(), sale_id=None, product_id=uuid4(), name="P1", quantity=1, price=10.0)],
        ),
        Sale(
            sale_id=uuid4(),
            date=datetime.now(),
            items=[SaleItem(sale_item_id=uuid4(), sale_id=None, product_id=uuid4(), name="P2", quantity=2, price=20.0)],
        ),
    ]
    for s in sales_to_add:
        sale_repo.add_sale(s)
    
    # Act
    sales = sale_repo.list_sales()
    
    # Assert
    assert len(sales) >= 2
    for s in sales_to_add:
        assert any(res.sale_id == s.sale_id for res in sales)


def test_persistence(sale_repo, session):
    # Arrange
    sale_id = uuid4()
    item_id = uuid4()
    item = SaleItem(
        sale_item_id=item_id,
        product_id=uuid4(), 
        name="Persistent Product", 
        selling_price=15.0, 
        quantity=1,
        price=15.0
    )
    sale = Sale(sale_id=sale_id, date=datetime.now(), items=[item], customer_name="Jane Doe")
    sale_repo.add_sale(sale)

    # Act
    # Create a new repository instance using the same session to test loading
    new_repo = SaleRepository(session)
    retrieved_sale = new_repo.get_sale(sale_id)

    # Assert
    assert retrieved_sale is not None
    assert retrieved_sale.sale_id == sale.sale_id



