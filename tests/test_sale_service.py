import pytest
from uuid import uuid4, UUID
from decimal import Decimal
from unittest.mock import Mock
from sqlalchemy.orm import Session

from sale.service import SaleService
from sale.models import Sale, SaleItem
from inventory.models import Product
from parties.models import Party, PartyType
from shared.exceptions import ProductNotFoundError

@pytest.fixture
def service(session):
    mock_ledger = Mock()
    
    from sale.repository import SaleRepository
    from inventory.repository import InventoryRepository
    from parties.repository import PartyRepository
    
    sale_repo = SaleRepository(session)
    inv_repo = InventoryRepository(session)
    party_repo = PartyRepository(session)
    
    return SaleService(sale_repo, inv_repo, party_repo, mock_ledger)

def test_record_sale_gst_intra_state(service, session):
    p_id = uuid4()
    product = Product(product_id=p_id, name="Laptop", selling_price=Decimal("1000"), quantity=10, gst_rate=Decimal("18"))
    session.add(product)
    
    party_id = uuid4()
    party = Party(party_id=party_id, name="Local Customer", party_type=PartyType.DEBTOR, balance=Decimal("0"), state="Karnataka")
    session.add(party)
    session.commit()
    
    items_data = [{'product_id': p_id, 'quantity': 1}] # Taxable 1000, GST 180 (90 CGST, 90 SGST)
    
    sale = service.record_sale(items_data, party_id=party_id)
    
    item = sale.items[0]
    assert item.cgst_amount == Decimal("90.00")
    assert item.sgst_amount == Decimal("90.00")
    assert item.igst_amount == Decimal("0.00")
    
    entries = service.ledger_service.record_transaction.call_args[0][1]
    accounts = [e['account'] for e in entries]
    assert 'Output CGST' in accounts
    assert 'Output SGST' in accounts
    assert 'Output IGST' not in accounts
    assert 'Sales Revenue' in accounts

def test_record_sale_gst_inter_state(service, session):
    p_id = uuid4()
    product = Product(product_id=p_id, name="Laptop", selling_price=Decimal("1000"), quantity=10, gst_rate=Decimal("18"))
    session.add(product)
    
    party_id = uuid4()
    party = Party(party_id=party_id, name="Outstate Customer", party_type=PartyType.DEBTOR, balance=Decimal("0"), state="Maharashtra")
    session.add(party)
    session.commit()
    
    items_data = [{'product_id': p_id, 'quantity': 1}] # Taxable 1000, GST 180 (180 IGST)
    
    sale = service.record_sale(items_data, party_id=party_id)
    
    item = sale.items[0]
    assert item.igst_amount == Decimal("180.00")
    assert item.cgst_amount == Decimal("0.00")
    assert item.sgst_amount == Decimal("0.00")
    
    entries = service.ledger_service.record_transaction.call_args[0][1]
    accounts = [e['account'] for e in entries]
    assert 'Output IGST' in accounts
    assert 'Output CGST' not in accounts
    assert 'Output SGST' not in accounts
    assert 'Sales Revenue' in accounts

def test_record_sale_insufficient_stock(service, session):
    p_id = uuid4()
    product = Product(product_id=p_id, name="Laptop", selling_price=Decimal("1000"), quantity=1, gst_rate=Decimal("18"))
    session.add(product)
    session.commit()
    
    items_data = [{'product_id': p_id, 'quantity': 2}]
    
    with pytest.raises(ValueError, match="Insufficient stock"):
        service.record_sale(items_data)

def test_record_sale_product_not_found(service):
    items_data = [{'product_id': uuid4(), 'quantity': 1}]
    with pytest.raises(ProductNotFoundError):
        service.record_sale(items_data)

def test_get_sale_not_found(service):
    with pytest.raises(ValueError, match="Sale not found"):
        service.get_sale(uuid4())

def test_delete_sale_reverses_stock_and_balance(service, session):
    p_id = uuid4()
    product = Product(product_id=p_id, name="Laptop", selling_price=Decimal("1000"), quantity=10, gst_rate=Decimal("18"))
    session.add(product)

    party_id = uuid4()
    party = Party(party_id=party_id, name="Customer", party_type=PartyType.DEBTOR, balance=Decimal("0"), state="Karnataka")
    session.add(party)
    session.commit()

    items_data = [{'product_id': p_id, 'quantity': 2}]
    sale = service.record_sale(items_data, party_id=party_id, paid_amount=Decimal("500"))

    assert product.quantity == 8
    assert sale.balance_amount == Decimal("1860")

    service.delete_sale(sale.sale_id)

    assert product.quantity == 10
    updated_party = session.get(Party, party_id)
    assert updated_party.balance == Decimal("0")
    with pytest.raises(ValueError, match="Sale not found"):
        service.get_sale(sale.sale_id)

def test_update_sale_creates_new_sale(service, session):
    p_id = uuid4()
    product = Product(product_id=p_id, name="Widget", selling_price=Decimal("100"), quantity=20, gst_rate=Decimal("18"))
    session.add(product)

    party_id = uuid4()
    party = Party(party_id=party_id, name="Client", party_type=PartyType.DEBTOR, balance=Decimal("0"), state="Karnataka")
    session.add(party)
    session.commit()

    items_data = [{'product_id': p_id, 'quantity': 3}]
    sale = service.record_sale(items_data, party_id=party_id)
    assert product.quantity == 17

    updated_items = [{'product_id': p_id, 'quantity': 1}]
    updated_sale = service.update_sale(sale.sale_id, updated_items, party_id=party_id)

    assert product.quantity == 19
    assert updated_sale.sale_id != sale.sale_id
    assert updated_sale.grand_total == Decimal("118")
