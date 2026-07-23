import pytest
from uuid import uuid4
from decimal import Decimal

from src.parties.repository import PartyRepository
from src.parties.service import PartyService


@pytest.fixture
def service(session):
    return PartyService(PartyRepository(session))


class TestListParties:
    def test_empty(self, client):
        resp = client.get("/api/parties")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_all(self, client, service):
        from src.parties.models import PartyType
        service.create_party("A", PartyType.DEBTOR, Decimal("100"))
        service.create_party("B", PartyType.CREDITOR, Decimal("200"))

        resp = client.get("/api/parties")
        data = resp.json()
        assert len(data) == 2

    def test_filter_by_type(self, client, service):
        from src.parties.models import PartyType
        service.create_party("Debtor A", PartyType.DEBTOR, Decimal("1000"))
        service.create_party("Creditor B", PartyType.CREDITOR, Decimal("500"))

        resp = client.get("/api/parties?party_type=DEBTOR")
        data = resp.json()
        assert len(data) == 1
        assert data[0]["name"] == "Debtor A"


class TestCreateParty:
    def test_creates(self, client):
        resp = client.post("/api/parties", json={
            "name": "New Party",
            "party_type": "DEBTOR",
            "balance": "1000",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "New Party"
        assert data["party_type"] == "DEBTOR"

    def test_empty_name(self, client):
        resp = client.post("/api/parties", json={
            "name": "",
            "party_type": "DEBTOR",
        })
        assert resp.status_code == 400


class TestGetParty:
    def test_not_found(self, client):
        resp = client.get(f"/api/parties/{uuid4()}")
        assert resp.status_code == 404

    def test_found(self, client, service):
        from src.parties.models import PartyType
        p = service.create_party("Test", PartyType.DEBTOR)
        resp = client.get(f"/api/parties/{p.party_id}")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Test"


class TestUpdateParty:
    def test_updates(self, client, service):
        from src.parties.models import PartyType
        p = service.create_party("Old", PartyType.DEBTOR)
        resp = client.put(f"/api/parties/{p.party_id}", json={
            "name": "New Name",
        })
        assert resp.status_code == 200
        assert resp.json()["name"] == "New Name"

    def test_not_found(self, client):
        resp = client.put(f"/api/parties/{uuid4()}", json={"name": "X"})
        assert resp.status_code == 404


class TestDeleteParty:
    def test_deletes(self, client, service):
        from src.parties.models import PartyType
        p = service.create_party("Delete Me", PartyType.DEBTOR)
        resp = client.delete(f"/api/parties/{p.party_id}")
        assert resp.status_code == 204

    def test_not_found(self, client):
        resp = client.delete(f"/api/parties/{uuid4()}")
        assert resp.status_code == 404


class TestAdjustBalance:
    def test_adjusts(self, client, service):
        from src.parties.models import PartyType
        p = service.create_party("Balance Test", PartyType.DEBTOR, Decimal("500"))
        resp = client.post(f"/api/parties/{p.party_id}/adjust-balance", json={
            "amount": "200",
        })
        assert resp.status_code == 200
        assert Decimal(resp.json()["balance"]) == Decimal("700")

    def test_not_found(self, client):
        resp = client.post(f"/api/parties/{uuid4()}/adjust-balance", json={
            "amount": "100",
        })
        assert resp.status_code == 404
