import pytest
from uuid import uuid4, UUID
from decimal import Decimal
from unittest.mock import Mock, patch
from dataclasses import dataclass

from sale.service import SaleService
from shared.exceptions import ProductNotFoundError

@dataclass
class ProductMock:
    product_id: UUID
    name: str
    selling_price: Decimal
    quantity: int

@dataclass
class PartyMock:
    party_id: UUID
    name: str
    balance: Decimal

@pytest.fixture
def mock_sale_repo(): return Mock()
@pytest.fixture
def mock_inv_repo(): return Mock()
@pytest.fixture
def mock_party_repo(): return Mock()
@pytest.fixture
def mock_ledger_service(): return Mock()

@pytest.fixture
def service(mock_sale_repo, mock_inv_repo, mock_party_repo, mock_ledger_service):
    return SaleService(mock_sale_repo, mock_inv_repo, mock_party_repo, mock_ledger_service)

def test_record_sale_success(service, mock_sale_repo, mock_inv_repo, mock_party_repo, mock_ledger_service):
    p_id = uuid4()
    product = ProductMock(p_id, "Laptop", Decimal("1000"), 10)
    mock_inv_repo.get_product.return_value = product
    
    party_id = uuid4()
    party = PartyMock(party_id, "Customer Inc", Decimal("0"))
    mock_party_repo.get_party.return_value = party
    
    items_data = [{'product_id': p_id, 'quantity': 1, 'tax_perc': 10}]
    
    with patch('sale.service.Sale') as MockSale:
        mock_sale_inst = MockSale.return_value
        mock_sale_inst.sale_id = uuid4()
        
        sale = service.record_sale(items_data, party_id=party_id, paid_amount=Decimal("500"))
        
        assert sale is not None
        mock_inv_repo.update_product.assert_called()
        mock_party_repo.update_balance.assert_called()
        mock_sale_repo.add_sale.assert_called()
        mock_ledger_service.record_transaction.assert_called()

def test_record_sale_insufficient_stock(service, mock_inv_repo):
    p_id = uuid4()
    product = ProductMock(p_id, "Laptop", Decimal("1000"), 1)
    mock_inv_repo.get_product.return_value = product
    
    items_data = [{'product_id': p_id, 'quantity': 2}]
    
    with pytest.raises(ValueError, match="Insufficient stock"):
        service.record_sale(items_data)

def test_list_sales(service, mock_sale_repo):
    mock_sale_repo.list_sales.return_value = [Mock(), Mock()]
    assert len(service.list_sales()) == 2

def test_get_sale_success(service, mock_sale_repo):
    s_id = uuid4()
    sale = Mock()
    mock_sale_repo.get_sale.return_value = sale
    assert service.get_sale(s_id) == sale
