import pytest
from uuid import uuid4, UUID
from decimal import Decimal
from unittest.mock import Mock, patch
from dataclasses import dataclass

from src.reports.service import ReportService

@pytest.fixture
def mock_inv_repo(): return Mock()
@pytest.fixture
def mock_party_repo(): return Mock()
@pytest.fixture
def mock_ledger_service(): return Mock()

@pytest.fixture
def service(mock_inv_repo, mock_party_repo, mock_ledger_service):
    return ReportService(mock_inv_repo, mock_party_repo, mock_ledger_service)

def test_get_trading_account(service, mock_ledger_service, mock_inv_repo):
    mock_ledger_service.get_balance.side_effect = lambda acc: Decimal("1000") if acc == "Sales Revenue" else Decimal("400") if acc == "Purchases" else Decimal("0")
    
    from dataclasses import dataclass
    @dataclass
    class ProductMock:
        quantity: int
        selling_price: Decimal
    
    mock_inv_repo.list_products.return_value = [ProductMock(10, Decimal("10"))] # 100 closing stock
    
    result = service.get_trading_account()
    
    assert result["sales"] == Decimal("1000")
    assert result["closing_stock"] == Decimal("100")
    assert result["purchases"] == Decimal("400")
    assert result["gross_profit"] == Decimal("700")

def test_get_profit_and_loss(service, mock_ledger_service):
    mock_ledger_service.get_balance.side_effect = lambda acc: Decimal("100") if acc == "Other Income" else Decimal("50") if acc == "Expenses" else Decimal("0")
    
    result = service.get_profit_and_loss(Decimal("700"))
    
    # Net Profit = (700 + 100) - 50 = 750
    assert result["net_profit"] == Decimal("750")

def test_get_balance_sheet(service, mock_ledger_service, mock_inv_repo, mock_party_repo):
    mock_ledger_service.get_balance.side_effect = lambda acc: Decimal("5000") if acc == "Cash" else Decimal("10000") if acc == "Capital" else Decimal("0")
    
    from dataclasses import dataclass
    @dataclass
    class ProductMock:
        quantity: int
        selling_price: Decimal
    mock_inv_repo.list_products.return_value = [ProductMock(10, Decimal("10"))] # 100 stock
    
    from dataclasses import dataclass
    @dataclass
    class PartyMock:
        balance: Decimal
    mock_party_repo.list_parties.return_value = [PartyMock(Decimal("200")), PartyMock(Decimal("-300"))]
    
    result = service.get_balance_sheet()
    
    assert result["assets"]["cash"] == Decimal("5000")
    assert result["assets"]["closing_stock"] == Decimal("100")
    assert result["assets"]["debtors"] == Decimal("200")
    assert result["assets"]["total"] == Decimal("5300")

def test_get_outstanding_report(service, mock_party_repo):
    from dataclasses import dataclass
    @dataclass
    class PartyMock:
        party_id: UUID
        name: str
        balance: Decimal
    
    mock_party_repo.list_parties.return_value = [
        PartyMock(uuid4(), "Customer A", Decimal("500")),
        PartyMock(uuid4(), "Supplier B", Decimal("-1000")),
        PartyMock(uuid4(), "Neutral Party", Decimal("0"))
    ]
    
    result = service.get_outstanding_report()
    
    assert len(result) == 2
    debtor = next(r for r in result if r["name"] == "Customer A")
    assert debtor["type"] == "Debtor"
    assert debtor["amount_due"] == Decimal("500")
    
    creditor = next(r for r in result if r["name"] == "Supplier B")
    assert creditor["type"] == "Creditor"
    assert creditor["amount_due"] == Decimal("1000")

def test_get_transaction_history(service, mock_ledger_service):
    mock_ledger_service.list_all_transactions.return_value = ["Tx1", "Tx2"]
    result = service.get_transaction_history()
    assert result == ["Tx1", "Tx2"]
