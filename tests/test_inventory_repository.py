import os
import pytest
from uuid import uuid4
from inventory.models import Product
from inventory.repository import InventoryRepository

@pytest.fixture
def repo():
    test_file = "test_inventory.json"
    repository = InventoryRepository(storage_file=test_file)
    yield repository
    if os.path.exists(test_file):
        os.remove(test_file)

def test_add_and_get_product(repo):
    # Arrange
    product_id = uuid4()
    product = Product(
        product_id=product_id,
        name="Test Product",
        selling_price=10.0,
        quantity=5,
        archived=False
    )

    # Act
    repo.add_product(product)
    retrieved_product = repo.get_product(product_id)

    # Assert
    assert retrieved_product is not None
    assert retrieved_product.name == "Test Product"
    assert retrieved_product.product_id == product_id
