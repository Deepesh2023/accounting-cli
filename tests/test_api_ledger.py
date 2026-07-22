from uuid import uuid4
from decimal import Decimal
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

from main import app
from api.deps import get_session
from ledger.repository import LedgerRepository
from ledger.service import LedgerService

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


def _clean_db():
    with _TEST_ENGINE.connect() as conn:
        for table in reversed(SQLModel.metadata.sorted_tables):
            conn.execute(table.delete())
        conn.commit()


def _ledger_service():
    return LedgerService(LedgerRepository(Session(_TEST_ENGINE)))


def _seed_entry(service, account: str, debit: str, credit: str, desc: str = ""):
    tx_id = uuid4()
    service.record_transaction(tx_id, [
        {"account": account, "debit": Decimal(debit), "credit": Decimal(credit), "desc": desc},
        {"account": "Offset", "debit": Decimal(credit), "credit": Decimal(debit), "desc": "offset"},
    ])


class TestListTransactions:
    def test_empty(self):
        _clean_db()
        app.dependency_overrides[get_session] = get_test_session
        c = TestClient(app)
        resp = c.get("/api/ledger/transactions")
        app.dependency_overrides.clear()
        assert resp.status_code == 200
        assert resp.json() == []

    def test_all(self):
        _clean_db()
        svc = _ledger_service()
        tx_id = uuid4()
        svc.record_transaction(tx_id, [
            {"account": "Sales Revenue", "debit": Decimal("0"), "credit": Decimal("1000")},
            {"account": "Cash", "debit": Decimal("1000"), "credit": Decimal("0")},
        ])
        app.dependency_overrides[get_session] = get_test_session
        c = TestClient(app)
        resp = c.get("/api/ledger/transactions")
        app.dependency_overrides.clear()
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2

    def test_filter_by_account(self):
        _clean_db()
        svc = _ledger_service()
        _seed_entry(svc, "Sales Revenue", "0", "500")
        _seed_entry(svc, "Purchases", "300", "0")
        app.dependency_overrides[get_session] = get_test_session
        c = TestClient(app)
        resp = c.get("/api/ledger/transactions?account_name=Sales Revenue")
        app.dependency_overrides.clear()
        assert resp.status_code == 200
        data = resp.json()
        assert all(e["account_name"] == "Sales Revenue" for e in data)


class TestAccountBalance:
    def test_returns_balance(self):
        _clean_db()
        svc = _ledger_service()
        _seed_entry(svc, "Cash", "1000", "0")
        app.dependency_overrides[get_session] = get_test_session
        c = TestClient(app)
        resp = c.get("/api/ledger/accounts/Cash/balance")
        app.dependency_overrides.clear()
        assert resp.status_code == 200
        data = resp.json()
        assert data["account"] == "Cash"
        assert Decimal(data["balance"]) == Decimal("1000")

    def test_zero_balance(self):
        _clean_db()
        app.dependency_overrides[get_session] = get_test_session
        c = TestClient(app)
        resp = c.get("/api/ledger/accounts/Unknown/balance")
        app.dependency_overrides.clear()
        assert resp.status_code == 200
        assert Decimal(resp.json()["balance"]) == Decimal("0")


class TestGstSummary:
    def test_returns_summary(self):
        _clean_db()
        svc = _ledger_service()
        _seed_entry(svc, "Input CGST", "100", "0")
        _seed_entry(svc, "Output CGST", "0", "180")
        app.dependency_overrides[get_session] = get_test_session
        c = TestClient(app)
        resp = c.get("/api/ledger/gst-summary")
        app.dependency_overrides.clear()
        assert resp.status_code == 200
        data = resp.json()
        assert "Input CGST" in data
        assert "Output CGST" in data
        assert Decimal(data["Input CGST"]) == Decimal("100")
        assert Decimal(data["Output CGST"]) == Decimal("-180")


class TestAccountBalances:
    def test_returns_multiple(self):
        _clean_db()
        svc = _ledger_service()
        _seed_entry(svc, "Cash", "5000", "0")
        _seed_entry(svc, "Bank", "10000", "0")
        app.dependency_overrides[get_session] = get_test_session
        c = TestClient(app)
        resp = c.get("/api/ledger/account-balances?accounts=Cash,Bank")
        app.dependency_overrides.clear()
        assert resp.status_code == 200
        data = resp.json()
        assert Decimal(data["Cash"]) == Decimal("5000")
        assert Decimal(data["Bank"]) == Decimal("10000")

    def test_empty_accounts_param(self):
        _clean_db()
        app.dependency_overrides[get_session] = get_test_session
        c = TestClient(app)
        resp = c.get("/api/ledger/account-balances?accounts=")
        app.dependency_overrides.clear()
        assert resp.status_code == 400
