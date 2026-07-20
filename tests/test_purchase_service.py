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
    gst_rate: Decimal = Decimal("0")

@dataclass
class PartyMock:
    party_id: UUID
    name: str
    balance: Decimal
    state: str = ""
    gstin: str = ""

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

def test_record_purchase_gst_intra_state(service, mock_purchase_repo, mock_inv_repo, mock_party_repo, mock_ledger_service):
    # Arrange: Party in Karnataka (same as company)
    p_id = uuid4()
    product = ProductMock(p_id, "Laptop", Decimal("1000"), 10, gst_rate=Decimal("18"))
    mock_inv_repo.get_product.return_value = product
    
    party_id = uuid4()
    party = PartyMock(party_id, "Local Supplier", Decimal("0"), state="Karnataka")
    mock_party_repo.get_party.return_value = party
    
    items_data = [{'product_id': p_id, 'quantity': 1}] # Taxable 1000, GST 180 (90 CGST, 90 SGST)
    
    with patch('purchase.service.Purchase') as MockPurchase:
        mock_purchase_inst = MockPurchase.return_value
        mock_purchase_inst.purchase_id = uuid4()
        
        service.record_purchase(items_data, party_id=party_id)
        
        # Check ledger entries for CGST and SGST
        entries = mock_ledger_service.record_transaction.call_args[0][1]
        accounts = [e['account'] for e in entries]
        assert 'Input CGST' in accounts
        assert 'Input SGST' in accounts
        assert 'Input IGST' not in accounts

def test_record_purchase_gst_inter_state(service, mock_purchase_repo, mock_inv_repo, mock_party_repo, mock_ledger_service):
    # Arrange: Party in Maharashtra (diff from Karnataka)
    p_id = uuid4()
    product = ProductMock(p_id, "Laptop", Decimal("1000"), 10, gst_rate=Decimal("18"))
    mock_inv_repo.get_product.return_value = product
    
    party_id = uuid4()
    party = PartyMock(party_id, "Outstate Supplier", Decimal("0"), state="Maharashtra")
    mock_party_repo.get_party.return_value = party
    
    items_data = [{'product_id': p_id, 'quantity': 1}] # Taxable 1000, GST 180 (180 IGST)
    
    with patch('purchase.service.Purchase') as MockPurchase:
        mock_purchase_inst = MockPurchase.return_value
        mock_purchase_inst.purchase_id = uuid4()
        
        service.record_purchase(items_data, party_id=party_id)
        
        # Check ledger entries for IGST
        entries = mock_ledger_service.record_transaction.call_args[0][1]
        accounts = [e['account'] for e in entries]
        assert 'Input IGST' in accounts
        assert 'Input CGST' not in accounts
        assert 'Input SGST' not in accounts

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
