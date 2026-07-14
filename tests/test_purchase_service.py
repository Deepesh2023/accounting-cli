import pytest
from uuid import uuid4, UUID
from decimal import Decimal
from unittest.mock import Mock, patch
from dataclasses import dataclass

from purchase.service import PurchaseService
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
def mock_purchase_repo(): return Mock()
@pytest.fixture
def mock_inv_repo(): return Mock()
@pytest.fixture
def mock_party_repo(): return Mock()
@pytest.fixture
def mock_ledger_service(): return Mock()

@pytest.fixture
def service(mock_purchase_repo, mock_inv_repo, mock_party_repo, mock_ledger_service):
    return PurchaseService(mock_purchase_repo, mock_inv_repo, mock_party_repo, mock_ledger_service)

def test_record_purchase_success(service, mock_purchase_repo, mock_inv_repo, mock_party_repo, mock_ledger_service):
    # Arrange
    p_id = uuid4()
    product = ProductMock(p_id, "Laptop", Decimal("1000"), 10)
    mock_inv_repo.get_product.return_value = product
    
    party_id = uuid4()
    party = PartyMock(party_id, "Supplier Inc", Decimal("0"))
    mock_party_repo.get_party.return_value = party
    
    items_data = [{'product_id': p_id, 'quantity': 2, 'tax_perc': 10}] # 2 * 1000 = 2000, tax 200, total 2200
    
    with patch('purchase.service.Purchase') as MockPurchase:
        mock_purchase_inst = MockPurchase.return_value
        mock_purchase_inst.purchase_id = uuid4()
        
        purchase = service.record_purchase(items_data, party_id=party_id, paid_amount=Decimal("1000"))
        
        # Assertions
        assert purchase is not None
        mock_inv_repo.update_product.assert_called()
        mock_party_repo.update_balance.assert_called()
        mock_purchase_repo.add_purchase.assert_called()
        mock_ledger_service.record_transaction.assert_called()

def test_record_purchase_product_not_found(service, mock_inv_repo):
    mock_inv_repo.get_product.return_value = None
    items_data = [{'product_id': uuid4(), 'quantity': 1}]
    
    with pytest.raises(ProductNotFoundError):
        service.record_purchase(items_data)

def test_list_purchases(service, mock_purchase_repo):
    mock_purchase_repo.list_purchases.return_value = [Mock(), Mock()]
    assert len(service.list_purchases()) == 2

def test_get_purchase_success(service, mock_purchase_repo):
    pur_id = uuid4()
    purchase = Mock()
    mock_purchase_repo.get_purchase.return_value = purchase
    assert service.get_purchase(pur_id) == purchase

def test_get_purchase_not_found(service, mock_purchase_repo):
    mock_purchase_repo.get_purchase.return_value = None
    with pytest.raises(ValueError, match="Purchase not found"):
        service.get_purchase(uuid4())
