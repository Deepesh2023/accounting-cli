import pytest
from uuid import uuid4
from decimal import Decimal
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

from main import app
from api.deps import get_parties_service, get_session
from parties.repository import PartyRepository
from parties.service import PartyService
from parties.models import PartyType

import inventory.models  # noqa: F401
import quotation.models  # noqa: F401
import sale.models  # noqa: F401
import parties.models  # noqa: F401
import expenses.models  # noqa: F401
import purchase.models  # noqa: F401
import ledger.models  # noqa: F401
import company.models  # noqa: F401

_TEST_ENGINE = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SQLModel.metadata.create_all(_TEST_ENGINE)


def get_test_session():
    with Session(_TEST_ENGINE) as session:
        yield session


@pytest.fixture(autouse=True)
def _clean_db():
    with _TEST_ENGINE.connect() as conn:
        for table in reversed(SQLModel.metadata.sorted_tables):
            conn.execute(table.delete())
        conn.commit()


@pytest.fixture
def service():
    return PartyService(PartyRepository(Session(_TEST_ENGINE)))


@pytest.fixture
def client():
    app.dependency_overrides[get_session] = get_test_session
    yield TestClient(app)
    app.dependency_overrides.clear()


class TestListParties:
    def test_empty(self, client):
        resp = client.get("/api/parties")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_all(self, client, service):
        service.create_party("Alice", PartyType.DEBTOR)
        service.create_party("Bob", PartyType.CREDITOR)

        resp = client.get("/api/parties")
        data = resp.json()
        assert len(data) == 2

    def test_filter_by_type(self, client, service):
        service.create_party("Alice", PartyType.DEBTOR)
        service.create_party("Bob", PartyType.CREDITOR)

        resp = client.get("/api/parties?party_type=DEBTOR")
        data = resp.json()
        assert len(data) == 1
        assert data[0]["name"] == "Alice"


class TestGetParty:
    def test_not_found(self, client):
        resp = client.get(f"/api/parties/{uuid4()}")
        assert resp.status_code == 404

    def test_found(self, client, service):
        p = service.create_party("Alice", PartyType.DEBTOR)
        resp = client.get(f"/api/parties/{p.party_id}")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Alice"


class TestCreateParty:
    def test_creates(self, client):
        resp = client.post("/api/parties", json={
            "name": "Acme Corp",
            "party_type": "CREDITOR",
            "balance": "1000.00",
            "phone": "1234567890",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Acme Corp"
        assert data["party_type"] == "CREDITOR"
        assert Decimal(data["balance"]) == Decimal("1000.00")

    def test_empty_name(self, client):
        resp = client.post("/api/parties", json={
            "name": "",
            "party_type": "DEBTOR",
        })
        assert resp.status_code == 400


class TestUpdateParty:
    def test_updates(self, client, service):
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
        p = service.create_party("Delete Me", PartyType.DEBTOR)
        resp = client.delete(f"/api/parties/{p.party_id}")
        assert resp.status_code == 204

        resp = client.get(f"/api/parties/{p.party_id}")
        assert resp.status_code == 404

    def test_not_found(self, client):
        resp = client.delete(f"/api/parties/{uuid4()}")
        assert resp.status_code == 404


class TestAdjustBalance:
    def test_adjusts(self, client, service):
        p = service.create_party("Acme", PartyType.DEBTOR, balance=Decimal("500"))
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
