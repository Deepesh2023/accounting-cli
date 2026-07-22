import pytest
from uuid import uuid4
from decimal import Decimal
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

from main import app
from api.deps import get_quotation_service, get_session
from quotation.repository import QuotationRepository
from quotation.service import QuotationService
from quotation.models import Quotation, QuotationItem

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
def session():
    with Session(_TEST_ENGINE) as session:
        yield session


@pytest.fixture
def service(session):
    repo = QuotationRepository(session)
    return QuotationService(repo)


@pytest.fixture
def client():
    app.dependency_overrides[get_session] = get_test_session
    yield TestClient(app)
    app.dependency_overrides.clear()


class TestListQuotations:
    def test_empty(self, client):
        resp = client.get("/api/quotations")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_all(self, client, service):
        q = Quotation(
            quotation_id=uuid4(),
            total_amount=Decimal("1000"),
            items=[
                QuotationItem(item_id=uuid4(), product_id=uuid4(), name="Widget",
                              quantity=2, unit_price=Decimal("500"), total_price=Decimal("1000")),
            ],
        )
        service.create_quotation(q)
        resp = client.get("/api/quotations")
        assert len(resp.json()) == 1


class TestGetQuotation:
    def test_not_found(self, client):
        resp = client.get(f"/api/quotations/{uuid4()}")
        assert resp.status_code == 404

    def test_found(self, client, service):
        q = Quotation(
            quotation_id=uuid4(),
            total_amount=Decimal("500"),
            items=[
                QuotationItem(item_id=uuid4(), product_id=uuid4(), name="Item A",
                              quantity=1, unit_price=Decimal("500"), total_price=Decimal("500")),
            ],
        )
        service.create_quotation(q)
        resp = client.get(f"/api/quotations/{q.quotation_id}")
        assert resp.status_code == 200
        assert resp.json()["total_amount"] == "500.0000000000"


class TestCreateQuotation:
    def test_creates(self, client):
        resp = client.post("/api/quotations", json={
            "items": [
                {"product_id": str(uuid4()), "name": "Widget", "quantity": 2, "unit_price": "250.00"},
            ],
            "notes": "Customer quote",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == "Widget"
        assert Decimal(data["total_amount"]) == Decimal("500.00")


class TestUpdateQuotation:
    def test_updates(self, client, service):
        q = Quotation(
            quotation_id=uuid4(),
            total_amount=Decimal("100"),
            items=[
                QuotationItem(item_id=uuid4(), product_id=uuid4(), name="Old",
                              quantity=1, unit_price=Decimal("100"), total_price=Decimal("100")),
            ],
        )
        service.create_quotation(q)
        resp = client.put(f"/api/quotations/{q.quotation_id}", json={
            "items": [
                {"product_id": str(uuid4()), "name": "New Item", "quantity": 3, "unit_price": "300.00"},
            ],
            "status": "Sent",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == "New Item"
        assert Decimal(data["total_amount"]) == Decimal("900.00")

    def test_not_found(self, client):
        resp = client.put(f"/api/quotations/{uuid4()}", json={
            "items": [
                {"product_id": str(uuid4()), "name": "X", "quantity": 1, "unit_price": "10.00"},
            ],
        })
        assert resp.status_code == 404


class TestDeleteQuotation:
    def test_deletes(self, client, service):
        q = Quotation(
            quotation_id=uuid4(),
            total_amount=Decimal("100"),
            items=[
                QuotationItem(item_id=uuid4(), product_id=uuid4(), name="Del",
                              quantity=1, unit_price=Decimal("100"), total_price=Decimal("100")),
            ],
        )
        service.create_quotation(q)
        resp = client.delete(f"/api/quotations/{q.quotation_id}")
        assert resp.status_code == 204

        resp = client.get(f"/api/quotations/{q.quotation_id}")
        assert resp.status_code == 404

    def test_not_found(self, client):
        resp = client.delete(f"/api/quotations/{uuid4()}")
        assert resp.status_code == 404
