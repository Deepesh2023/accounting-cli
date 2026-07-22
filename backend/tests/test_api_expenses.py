import pytest
from uuid import uuid4
from decimal import Decimal

from expenses.repository import ExpenseRepository
from expenses.service import ExpenseService
from ledger.service import LedgerService
from ledger.repository import LedgerRepository


@pytest.fixture
def service(session):
    repo = ExpenseRepository(session)
    ledger_svc = LedgerService(LedgerRepository(session))
    return ExpenseService(repo, ledger_service=ledger_svc)


class TestListExpenses:
    def test_empty(self, client):
        resp = client.get("/api/expenses")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_all(self, client, service):
        service.record_expense("Rent", Decimal("5000"), paid_by="Cash")
        service.record_expense("Salary", Decimal("30000"), paid_by="Bank")

        resp = client.get("/api/expenses")
        data = resp.json()
        assert len(data) == 2

    def test_filter_by_category(self, client, service):
        service.record_expense("Rent", Decimal("5000"), paid_by="Cash")

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
        recorded = service.record_expense("Rent", Decimal("5000"), paid_by="Cash")
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
        recorded = service.record_expense("Rent", Decimal("5000"), paid_by="Cash")
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
        recorded = service.record_expense("Rent", Decimal("5000"), paid_by="Cash")
        resp = client.delete(f"/api/expenses/{recorded.expense_id}")
        assert resp.status_code == 204

        resp = client.get(f"/api/expenses/{recorded.expense_id}")
        assert resp.status_code == 404

    def test_not_found(self, client):
        resp = client.delete(f"/api/expenses/{uuid4()}")
        assert resp.status_code == 404
