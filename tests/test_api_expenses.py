import pytest
from uuid import uuid4
from decimal import Decimal
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

from main import app
from api.deps import get_expense_service, get_session
from expenses.repository import ExpenseRepository
from expenses.service import ExpenseService
from expenses.models import Expense
from ledger.service import LedgerService
from ledger.repository import LedgerRepository

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
    repo = ExpenseRepository(session)
    ledger_svc = LedgerService(LedgerRepository(session))
    return ExpenseService(repo, ledger_service=ledger_svc)


@pytest.fixture
def client():
    app.dependency_overrides[get_session] = get_test_session
    yield TestClient(app)
    app.dependency_overrides.clear()


class TestListExpenses:
    def test_empty(self, client):
        resp = client.get("/api/expenses")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_all(self, client, service):
        e1 = Expense(category="Rent", paid_by="Cash", amount=Decimal("5000"))
        e2 = Expense(category="Salary", paid_by="Bank", amount=Decimal("30000"))
        service.record_expense(e1)
        service.record_expense(e2)

        resp = client.get("/api/expenses")
        data = resp.json()
        assert len(data) == 2

    def test_filter_by_category(self, client, service):
        e1 = Expense(category="Rent", paid_by="Cash", amount=Decimal("5000"))
        service.record_expense(e1)

        resp = client.get("/api/expenses?category=Rent")
        data = resp.json()
        assert len(data) == 1

        resp = client.get("/api/expenses?category=Other")
        assert len(resp.json()) == 0


class TestGetExpense:
    def test_not_found(self, client):
        resp = client.get(f"/api/expenses/{uuid4()}")
        assert resp.status_code == 404

    def test_found(self, client, service):
        e = Expense(category="Rent", paid_by="Cash", amount=Decimal("5000"))
        recorded = service.record_expense(e)
        resp = client.get(f"/api/expenses/{recorded.expense_id}")
        assert resp.status_code == 200
        assert resp.json()["category"] == "Rent"
        assert Decimal(resp.json()["amount"]) == Decimal("5000")


class TestCreateExpense:
    def test_creates(self, client):
        resp = client.post("/api/expenses", json={
            "category": "Utilities",
            "paid_by": "Cash",
            "amount": "1500.00",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["category"] == "Utilities"
        assert Decimal(data["amount"]) == Decimal("1500.00")


class TestUpdateExpense:
    def test_updates(self, client, service):
        e = Expense(category="Rent", paid_by="Cash", amount=Decimal("5000"))
        recorded = service.record_expense(e)
        resp = client.put(f"/api/expenses/{recorded.expense_id}", json={
            "category": "Rent Updated",
            "paid_by": "Bank",
            "amount": "5500.00",
        })
        assert resp.status_code == 200
        assert resp.json()["category"] == "Rent Updated"
        assert Decimal(resp.json()["amount"]) == Decimal("5500.00")

    def test_not_found(self, client):
        resp = client.put(f"/api/expenses/{uuid4()}", json={
            "category": "Test",
            "paid_by": "Cash",
            "amount": "100.00",
        })
        assert resp.status_code == 404


class TestDeleteExpense:
    def test_deletes(self, client, service):
        e = Expense(category="Rent", paid_by="Cash", amount=Decimal("5000"))
        recorded = service.record_expense(e)
        resp = client.delete(f"/api/expenses/{recorded.expense_id}")
        assert resp.status_code == 204

        resp = client.get(f"/api/expenses/{recorded.expense_id}")
        assert resp.status_code == 404

    def test_not_found(self, client):
        resp = client.delete(f"/api/expenses/{uuid4()}")
        assert resp.status_code == 404
