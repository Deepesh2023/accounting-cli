import pytest
from uuid import uuid4, UUID
from decimal import Decimal
from unittest.mock import Mock, patch
from dataclasses import dataclass

from inventory.service import InventoryService
from shared.exceptions import ProductNotFoundError, InvalidProductDataError

@dataclass
class ProductMock:
    product_id: UUID
    name: str
    selling_price: Decimal
    gst_rate: Decimal = Decimal("0.0")
    hsn_code: str = ""
    quantity: int = 0
    archived: bool = False

@pytest.fixture
def mock_repo():
    return Mock()

@pytest.fixture
def service(mock_repo):
    return InventoryService(mock_repo)

def test_list_products(service, mock_repo):
    p1 = ProductMock(product_id=uuid4(), name="P1", selling_price=Decimal("10"), quantity=5, archived=False)
    p2 = ProductMock(product_id=uuid4(), name="P2", selling_price=Decimal("20"), quantity=10, archived=True)
    mock_repo.list_products.return_value = [p1, p2]

    assert service.list_products(show_archived=False) == [p1]
    assert service.list_products(show_archived=True) == [p2]

def test_add_product_success(service, mock_repo):
    import inventory.service
    with patch('inventory.service.Product') as MockProduct:
        mock_product_inst = MockProduct.return_value
        mock_product_inst.name = "Test Product"
        
        product = service.add_product("Test Product", 10.5, 100, gst_rate=18, hsn_code="1234")

        assert product.name == "Test Product"
        mock_repo.add_product.assert_called_once_with(mock_product_inst)

def test_add_product_negative_gst(service):
    with pytest.raises(InvalidProductDataError):
        service.add_product("Bad", 10, 10, gst_rate=-1)

def test_add_product_negative_qty(service):
    with pytest.raises(InvalidProductDataError):
        service.add_product("Bad", 10, -1)

def test_get_product_success(service, mock_repo):
    p_id = uuid4()
    product = ProductMock(product_id=p_id, name="P1", selling_price=Decimal("10"), quantity=5)
    mock_repo.get_product.return_value = product

    assert service.get_product(p_id) == product

def test_get_product_not_found(service, mock_repo):
    mock_repo.get_product.return_value = None
    with pytest.raises(ProductNotFoundError):
        service.get_product(uuid4())

def test_change_visibility_success(service, mock_repo):
    p_id = uuid4()
    product = ProductMock(product_id=p_id, name="P1", selling_price=Decimal("10"), quantity=5)
    mock_repo.change_visibility.return_value = product

    assert service.change_visibility(p_id) == product

def test_change_visibility_not_found(service, mock_repo):
    mock_repo.change_visibility.return_value = None
    with pytest.raises(ProductNotFoundError):
        service.change_visibility(uuid4())

def test_update_product(service, mock_repo):
    product = ProductMock(product_id=uuid4(), name="P1", selling_price=Decimal("10"), quantity=5)
    service.update_product(product)
    mock_repo.update_product.assert_called_once_with(product)

def test_search_products(service, mock_repo):
    p1 = ProductMock(product_id=uuid4(), name="Apple", selling_price=Decimal("10"), quantity=5)
    mock_repo.search_products.return_value = [p1]

    assert service.search_products("Apple") == [p1]
    mock_repo.search_products.assert_called_once_with("Apple")

def test_delete_product_success(service, mock_repo):
    p_id = uuid4()
    mock_repo.delete_product.return_value = True
    result = service.delete_product(p_id)
    assert result is True
    mock_repo.delete_product.assert_called_once_with(p_id)

def test_delete_product_not_found(service, mock_repo):
    mock_repo.delete_product.return_value = False
    result = service.delete_product(uuid4())
    assert result is False
