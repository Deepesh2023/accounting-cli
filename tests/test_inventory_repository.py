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

def test_list_and_search_products(repo):
    # Arrange
    p1_id = uuid4()
    p1 = Product(product_id=p1_id, name="Apple", selling_price=1.0, quantity=10)
    p2_id = uuid4()
    p2 = Product(product_id=p2_id, name="Banana", selling_price=0.5, quantity=20)
    
    repo.add_product(p1)
    repo.add_product(p2)

    # Test List
    products = repo.list_products()
    assert len(products) == 2
    assert p1 in products
    assert p2 in products

    # Test Search by Name
    search_apple = repo.search_products("Apple")
    assert len(search_apple) == 1
    assert search_apple[0].product_id == p1_id

    # Test Search by ID
    search_id = repo.search_products(str(p2_id))
    assert len(search_id) == 1
    assert search_id[0].product_id == p2_id

    # Test Search Case Insensitive
    search_case = repo.search_products("apple")
    assert len(search_case) == 1
    assert search_case[0].product_id == p1_id
