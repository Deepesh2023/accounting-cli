import pytest
from uuid import uuid4
from decimal import Decimal
from quotation.models import Quotation, QuotationItem
from quotation.repository import QuotationRepository
from quotation.service import QuotationService

def test_quotation_lifecycle(session):
    # Arrange
    repo = QuotationRepository(session)
    service = QuotationService(repo)
    
    item = QuotationItem(
        product_id=uuid4(),
        name="Test Product",
        quantity=2,
        unit_price=Decimal("100.00"),
        total_price=Decimal("200.00")
    )
    
    quotation = Quotation(
        total_amount=Decimal("200.00"),
        status="Draft",
        items=[item]
    )
    
    # Act - Create
    created = service.create_quotation(quotation)
    assert created.quotation_id is not None
    
    # Act - List
    all_qs = service.get_all_quotations()
    assert len(all_qs) == 1
    assert all_qs[0].total_amount == Decimal("200.00")
    
    # Act - Retrieve
    retrieved = service.get_quotation_by_id(created.quotation_id)
    assert retrieved is not None
    assert len(retrieved.items) == 1
    assert retrieved.items[0].name == "Test Product"
    
    # Act - Delete
    success = service.remove_quotation(created.quotation_id)
    assert success is True
    assert len(service.get_all_quotations()) == 0
