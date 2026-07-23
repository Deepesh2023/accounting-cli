import pytest
from uuid import uuid4
from decimal import Decimal

from src.quotation.repository import QuotationRepository
from src.quotation.service import QuotationService
from src.quotation.models import Quotation, QuotationItem


@pytest.fixture
def service(session):
    return QuotationService(QuotationRepository(session))


class TestListQuotations:
    def test_empty(self, client):
        resp = client.get("/api/quotations")
        assert resp.status_code == 200
        assert resp.json() == []


class TestCreateQuotation:
    def test_creates(self, client):
        resp = client.post("/api/quotations", json={
            "items": [{"product_id": str(uuid4()), "name": "Item A", "quantity": 2, "unit_price": "100"}],
            "notes": "Test quote",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == "Item A"
        assert Decimal(data["total_amount"]) == Decimal("200")

    def test_without_items(self, client):
        resp = client.post("/api/quotations", json={
            "items": [],
        })
        assert resp.status_code == 201
        assert Decimal(resp.json()["total_amount"]) == Decimal("0")


class TestGetQuotation:
    def test_not_found(self, client):
        resp = client.get(f"/api/quotations/{uuid4()}")
        assert resp.status_code == 404

    def test_found(self, client, service):
        items = [QuotationItem(item_id=uuid4(), product_id=uuid4(), name="Test", quantity=1, unit_price=Decimal("50"), total_price=Decimal("50"))]
        q = Quotation(quotation_id=uuid4(), total_amount=Decimal("50"), items=items)
        for item in items:
            item.quotation_id = q.quotation_id
        service.create_quotation(q)
        resp = client.get(f"/api/quotations/{q.quotation_id}")
        assert resp.status_code == 200


class TestUpdateQuotation:
    def test_updates(self, client, service):
        items = [QuotationItem(item_id=uuid4(), product_id=uuid4(), name="Old", quantity=1, unit_price=Decimal("50"), total_price=Decimal("50"))]
        q = Quotation(quotation_id=uuid4(), total_amount=Decimal("50"), items=items)
        for item in items:
            item.quotation_id = q.quotation_id
        service.create_quotation(q)

        resp = client.put(f"/api/quotations/{q.quotation_id}", json={
            "items": [{"product_id": str(uuid4()), "name": "Updated", "quantity": 3, "unit_price": "200"}],
            "notes": "Updated quote",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["items"][0]["name"] == "Updated"
        assert Decimal(data["total_amount"]) == Decimal("600")

    def test_not_found(self, client):
        resp = client.put(f"/api/quotations/{uuid4()}", json={
            "items": [{"product_id": str(uuid4()), "name": "X", "quantity": 1, "unit_price": "10"}],
        })
        assert resp.status_code == 404


class TestDeleteQuotation:
    def test_deletes(self, client, service):
        items = [QuotationItem(item_id=uuid4(), product_id=uuid4(), name="Del", quantity=1, unit_price=Decimal("10"), total_price=Decimal("10"))]
        q = Quotation(quotation_id=uuid4(), total_amount=Decimal("10"), items=items)
        for item in items:
            item.quotation_id = q.quotation_id
        service.create_quotation(q)
        resp = client.delete(f"/api/quotations/{q.quotation_id}")
        assert resp.status_code == 204

    def test_not_found(self, client):
        resp = client.delete(f"/api/quotations/{uuid4()}")
        assert resp.status_code == 404
