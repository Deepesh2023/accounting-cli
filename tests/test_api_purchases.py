import pytest
from uuid import uuid4
from decimal import Decimal

from purchase.repository import PurchaseRepository
from purchase.service import PurchaseService
from inventory.repository import InventoryRepository
from inventory.models import Product
from parties.repository import PartyRepository
from parties.models import Party, PartyType
from ledger.service import LedgerService
from ledger.repository import LedgerRepository


@pytest.fixture
def product(session):
    p = Product(product_id=uuid4(), name="Widget", selling_price=Decimal("100"), quantity=10, gst_rate=Decimal("18"))
    session.add(p)
    session.commit()
    return p


@pytest.fixture
def party(session):
    p = Party(party_id=uuid4(), name="Supplier Co", party_type=PartyType.CREDITOR, balance=Decimal("0"), state="Karnataka")
    session.add(p)
    session.commit()
    return p


@pytest.fixture
def service(session):
    purchase_repo = PurchaseRepository(session)
    inv_repo = InventoryRepository(session)
    party_repo = PartyRepository(session)
    ledger_svc = LedgerService(LedgerRepository(session))
    return PurchaseService(purchase_repo, inv_repo, party_repo, ledger_svc)


class TestListPurchases:
    def test_empty(self, client):
        resp = client.get("/api/purchases")
        assert resp.status_code == 200
        assert resp.json() == []


class TestCreatePurchase:
    def test_with_party(self, client, product, party):
        resp = client.post("/api/purchases", json={
            "items_data": [{"product_id": str(product.product_id), "quantity": 5, "price": "80"}],
            "party_id": str(party.party_id),
            "paid_amount": "200.00",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["quantity"] == 5
        assert Decimal(data["grand_total"]) > Decimal("0")

    def test_without_party(self, client, product):
        resp = client.post("/api/purchases", json={
            "items_data": [{"product_id": str(product.product_id), "quantity": 2, "price": "100"}],
            "paid_amount": "236.00",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert len(data["items"]) == 1
        assert data["party_id"] is None

    def test_unknown_product(self, client):
        resp = client.post("/api/purchases", json={
            "items_data": [{"product_id": str(uuid4()), "quantity": 1, "price": "50"}],
        })
        assert resp.status_code == 400


class TestGetPurchase:
    def test_not_found(self, client):
        resp = client.get(f"/api/purchases/{uuid4()}")
        assert resp.status_code == 404

    def test_found(self, client, product, party, service):
        purchase = service.record_purchase(
            [{"product_id": product.product_id, "quantity": 1, "price": Decimal("100")}],
            party_id=party.party_id,
        )
        resp = client.get(f"/api/purchases/{purchase.purchase_id}")
        assert resp.status_code == 200
        assert resp.json()["purchase_id"] == str(purchase.purchase_id)


class TestDeletePurchase:
    def test_deletes(self, client, product, party, service):
        purchase = service.record_purchase(
            [{"product_id": product.product_id, "quantity": 1, "price": Decimal("100")}],
            party_id=party.party_id,
        )
        resp = client.delete(f"/api/purchases/{purchase.purchase_id}")
        assert resp.status_code == 204

        resp = client.get(f"/api/purchases/{purchase.purchase_id}")
        assert resp.status_code == 404

    def test_not_found(self, client):
        resp = client.delete(f"/api/purchases/{uuid4()}")
        assert resp.status_code == 404


class TestRecordPayment:
    def test_payment(self, client, product, party, service):
        purchase = service.record_purchase(
            [{"product_id": product.product_id, "quantity": 2, "price": Decimal("100")}],
            party_id=party.party_id,
        )
        resp = client.post(f"/api/purchases/{purchase.purchase_id}/payment", json={
            "amount": "50.00",
        })
        assert resp.status_code == 200
        assert Decimal(resp.json()["paid_amount"]) > Decimal(str(purchase.paid_amount))
