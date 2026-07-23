from uuid import uuid4
from decimal import Decimal

from src.ledger.repository import LedgerRepository
from src.ledger.service import LedgerService


def _ledger_service(session):
    return LedgerService(LedgerRepository(session))


def _seed_entry(service, account: str, debit: str, credit: str, desc: str = ""):
    tx_id = uuid4()
    service.record_transaction(tx_id, [
        {"account": account, "debit": Decimal(debit), "credit": Decimal(credit), "desc": desc},
        {"account": "Offset", "debit": Decimal(credit), "credit": Decimal(debit), "desc": "offset"},
    ])


def test_list_transactions_empty(client):
    resp = client.get("/api/ledger/transactions")
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_transactions_all(client, session):
    svc = _ledger_service(session)
    _seed_entry(svc, "Cash", "1000", "0", "Sale")
    _seed_entry(svc, "Bank", "0", "500", "Payment")

    resp = client.get("/api/ledger/transactions")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 4


def test_list_transactions_filter(client, session):
    svc = _ledger_service(session)
    _seed_entry(svc, "Sales Revenue", "0", "500")
    _seed_entry(svc, "Purchases", "300", "0")

    resp = client.get("/api/ledger/transactions?account_name=Sales Revenue")
    assert resp.status_code == 200
    data = resp.json()
    assert all(e["account_name"] == "Sales Revenue" for e in data)


def test_account_balance(client, session):
    svc = _ledger_service(session)
    _seed_entry(svc, "Cash", "1000", "0")
    _seed_entry(svc, "Cash", "500", "0")
    _seed_entry(svc, "Cash", "0", "200")

    resp = client.get("/api/ledger/accounts/Cash/balance")
    assert resp.status_code == 200
    assert resp.json()["account"] == "Cash"
    assert Decimal(resp.json()["balance"]) == Decimal("1300")


def test_account_balance_zero(client):
    resp = client.get("/api/ledger/accounts/Unknown/balance")
    assert resp.status_code == 200
    assert Decimal(resp.json()["balance"]) == Decimal("0")


def test_gst_summary(client, session):
    svc = _ledger_service(session)
    _seed_entry(svc, "Output CGST", "0", "90")
    _seed_entry(svc, "Output SGST", "0", "90")
    _seed_entry(svc, "Input CGST", "50", "0")

    resp = client.get("/api/ledger/gst-summary")
    assert resp.status_code == 200
    data = resp.json()
    assert Decimal(data["Output CGST"]) == Decimal("-90")
    assert Decimal(data["Input CGST"]) == Decimal("50")


def test_account_balances(client, session):
    svc = _ledger_service(session)
    _seed_entry(svc, "Cash", "5000", "0")
    _seed_entry(svc, "Bank", "0", "1000")

    resp = client.get("/api/ledger/account-balances?accounts=Cash,Bank")
    assert resp.status_code == 200
    data = resp.json()
    assert Decimal(data["Cash"]) == Decimal("5000")
    assert Decimal(data["Bank"]) == Decimal("-1000")


def test_account_balances_empty(client):
    resp = client.get("/api/ledger/account-balances?accounts=")
    assert resp.status_code == 400
