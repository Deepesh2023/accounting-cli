import pytest
from uuid import uuid4
from decimal import Decimal

from src.sale.repository import SaleRepository
from src.sale.service import SaleService
from src.inventory.repository import InventoryRepository
from src.inventory.models import Product
from src.parties.repository import PartyRepository
from src.parties.models import Party, PartyType
from src.ledger.service import LedgerService
from src.ledger.repository import LedgerRepository


@pytest.fixture
def product(session):
    p = Product(product_id=uuid4(), name="Widget", selling_price=Decimal("100"), quantity=50, gst_rate=Decimal("18"))
    session.add(p)
    session.commit()
    return p


@pytest.fixture
def party(session):
    p = Party(party_id=uuid4(), name="Acme Corp", party_type=PartyType.DEBTOR, balance=Decimal("0"), state="Karnataka")
    session.add(p)
    session.commit()
    return p


@pytest.fixture
def service(session):
    sale_repo = SaleRepository(session)
    inv_repo = InventoryRepository(session)
    party_repo = PartyRepository(session)
    ledger_svc = LedgerService(LedgerRepository(session))
    return SaleService(sale_repo, inv_repo, party_repo, ledger_svc)


class TestListSales:
    def test_empty(self, client):
        resp = client.get("/api/sales")
        assert resp.status_code == 200
        assert resp.json() == []


class TestCreateSale:
    def test_with_party(self, client, product, party):
        resp = client.post("/api/sales", json={
            "items_data": [{"product_id": str(product.product_id), "quantity": 2}],
            "party_id": str(party.party_id),
            "paid_amount": "50.00",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == "Widget"
        assert data["items"][0]["quantity"] == 2
        assert Decimal(data["grand_total"]) > Decimal("0")
        assert Decimal(data["paid_amount"]) == Decimal("50.00")
        assert Decimal(data["balance_amount"]) == Decimal(data["grand_total"]) - Decimal("50.00")

    def test_without_party(self, client, product):
        resp = client.post("/api/sales", json={
            "items_data": [{"product_id": str(product.product_id), "quantity": 1}],
            "paid_amount": "118.00",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert len(data["items"]) == 1
        assert data["party_id"] is None

    def test_insufficient_stock(self, client, product):
        resp = client.post("/api/sales", json={
            "items_data": [{"product_id": str(product.product_id), "quantity": 999}],
        })
        assert resp.status_code == 400

    def test_unknown_product(self, client):
        resp = client.post("/api/sales", json={
            "items_data": [{"product_id": str(uuid4()), "quantity": 1}],
        })
        assert resp.status_code == 400


class TestGetSale:
    def test_not_found(self, client):
        resp = client.get(f"/api/sales/{uuid4()}")
        assert resp.status_code == 404

    def test_found(self, client, product, party, service):
        sale = service.record_sale(
            [{"product_id": product.product_id, "quantity": 1}],
            party_id=party.party_id,
        )
        resp = client.get(f"/api/sales/{sale.sale_id}")
        assert resp.status_code == 200
        assert resp.json()["sale_id"] == str(sale.sale_id)


class TestDeleteSale:
    def test_deletes(self, client, product, party, service):
        sale = service.record_sale(
            [{"product_id": product.product_id, "quantity": 1}],
            party_id=party.party_id,
        )
        resp = client.delete(f"/api/sales/{sale.sale_id}")
        assert resp.status_code == 204

        resp = client.get(f"/api/sales/{sale.sale_id}")
        assert resp.status_code == 404

    def test_not_found(self, client):
        resp = client.delete(f"/api/sales/{uuid4()}")
        assert resp.status_code == 404


class TestRecordPayment:
    def test_payment(self, client, product, party, service):
        sale = service.record_sale(
            [{"product_id": product.product_id, "quantity": 2}],
            party_id=party.party_id,
        )
        resp = client.post(f"/api/sales/{sale.sale_id}/payment", json={
            "amount": "50.00",
        })
        assert resp.status_code == 200
        assert Decimal(resp.json()["paid_amount"]) > Decimal(str(sale.paid_amount))
