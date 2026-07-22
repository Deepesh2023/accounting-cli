import pytest
from uuid import uuid4, UUID
from decimal import Decimal
from unittest.mock import Mock
from sqlalchemy.orm import Session

from purchase.service import PurchaseService
from purchase.models import Purchase, PurchaseItem
from inventory.models import Product
from parties.models import Party, PartyType
from shared.exceptions import ProductNotFoundError

@pytest.fixture
def service(session):
    # We still mock the ledger service because it's a separate domain 
    # and we want to verify the calls without setting up the whole ledger DB
    mock_ledger = Mock()
    
    from purchase.repository import PurchaseRepository
    from inventory.repository import InventoryRepository
    from parties.repository import PartyRepository
    
    pur_repo = PurchaseRepository(session)
    inv_repo = InventoryRepository(session)
    party_repo = PartyRepository(session)
    
    return PurchaseService(pur_repo, inv_repo, party_repo, mock_ledger)

def test_record_purchase_gst_intra_state(service, session):
    # Arrange: Party in Karnataka (same as company)
    p_id = uuid4()
    product = Product(product_id=p_id, name="Laptop", selling_price=Decimal("1000"), quantity=10, gst_rate=Decimal("18"))
    session.add(product)
    
    party_id = uuid4()
    party = Party(party_id=party_id, name="Local Supplier", party_type=PartyType.CREDITOR, balance=Decimal("0"), state="Karnataka")
    session.add(party)
    session.commit()
    
    items_data = [{'product_id': p_id, 'quantity': 1}] # Taxable 1000, GST 180 (90 CGST, 90 SGST)
    
    purchase = service.record_purchase(items_data, party_id=party_id)
    
    # Verify GST Split in PurchaseItems
    item = purchase.items[0]
    assert item.cgst_amount == Decimal("90.00")
    assert item.sgst_amount == Decimal("90.00")
    assert item.igst_amount == Decimal("0.00")
    
    # Verify Ledger entries
    entries = service.ledger_service.record_transaction.call_args[0][1]
    accounts = [e['account'] for e in entries]
    assert 'Input CGST' in accounts
    assert 'Input SGST' in accounts
    assert 'Input IGST' not in accounts

def test_record_purchase_gst_inter_state(service, session):
    # Arrange: Party in Maharashtra (diff from Karnataka)
    p_id = uuid4()
    product = Product(product_id=p_id, name="Laptop", selling_price=Decimal("1000"), quantity=10, gst_rate=Decimal("18"))
    session.add(product)
    
    party_id = uuid4()
    party = Party(party_id=party_id, name="Outstate Supplier", party_type=PartyType.CREDITOR, balance=Decimal("0"), state="Maharashtra")
    session.add(party)
    session.commit()
    
    items_data = [{'product_id': p_id, 'quantity': 1}] # Taxable 1000, GST 180 (180 IGST)
    
    purchase = service.record_purchase(items_data, party_id=party_id)
    
    # Verify GST Split
    item = purchase.items[0]
    assert item.igst_amount == Decimal("180.00")
    assert item.cgst_amount == Decimal("0.00")
    assert item.sgst_amount == Decimal("0.00")
    
    # Verify Ledger
    entries = service.ledger_service.record_transaction.call_args[0][1]
    accounts = [e['account'] for e in entries]
    assert 'Input IGST' in accounts
    assert 'Input CGST' not in accounts
    assert 'Input SGST' not in accounts

def test_record_purchase_product_not_found(service):
    items_data = [{'product_id': uuid4(), 'quantity': 1}]
    with pytest.raises(ProductNotFoundError):
        service.record_purchase(items_data)

def test_get_purchase_not_found(service):
    with pytest.raises(ValueError, match="Purchase not found"):
        service.get_purchase(uuid4())

def test_delete_purchase_reverses_stock_and_balance(service, session):
    p_id = uuid4()
    product = Product(product_id=p_id, name="Raw Material", selling_price=Decimal("500"), quantity=10, gst_rate=Decimal("18"))
    session.add(product)

    party_id = uuid4()
    party = Party(party_id=party_id, name="Supplier", party_type=PartyType.CREDITOR, balance=Decimal("0"), state="Karnataka")
    session.add(party)
    session.commit()

    items_data = [{'product_id': p_id, 'quantity': 5}]
    purchase = service.record_purchase(items_data, party_id=party_id, paid_amount=Decimal("1000"))

    assert product.quantity == 15

    service.delete_purchase(purchase.purchase_id)

    assert product.quantity == 10
    updated_party = session.get(Party, party_id)
    assert updated_party.balance == Decimal("0")
    with pytest.raises(ValueError, match="Purchase not found"):
        service.get_purchase(purchase.purchase_id)

def test_update_purchase_creates_new_purchase(service, session):
    p_id = uuid4()
    product = Product(product_id=p_id, name="Material", selling_price=Decimal("200"), quantity=30, gst_rate=Decimal("18"))
    session.add(product)

    party_id = uuid4()
    party = Party(party_id=party_id, name="Vendor", party_type=PartyType.CREDITOR, balance=Decimal("0"), state="Karnataka")
    session.add(party)
    session.commit()

    items_data = [{'product_id': p_id, 'quantity': 10}]
    purchase = service.record_purchase(items_data, party_id=party_id)
    assert product.quantity == 40

    updated_items = [{'product_id': p_id, 'quantity': 2}]
    updated_purchase = service.update_purchase(purchase.purchase_id, updated_items, party_id=party_id)

    assert product.quantity == 32
    assert updated_purchase.purchase_id != purchase.purchase_id
    assert updated_purchase.grand_total == Decimal("472")

