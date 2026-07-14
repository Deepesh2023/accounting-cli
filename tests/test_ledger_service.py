import pytest
from uuid import uuid4, UUID
from decimal import Decimal
from unittest.mock import Mock

from ledger.models import LedgerEntry
from ledger.service import LedgerService

@pytest.fixture
def mock_repo():
    return Mock()

@pytest.fixture
def service(mock_repo):
    return LedgerService(mock_repo)

def test_record_transaction_success(service, mock_repo):
    tx_id = uuid4()
    entries = [
        {'account': 'Cash', 'debit': Decimal("100"), 'credit': Decimal("0"), 'desc': 'Payment'},
        {'account': 'Sales', 'debit': Decimal("0"), 'credit': Decimal("100"), 'desc': 'Sale'}
    ]
    
    service.record_transaction(tx_id, entries)
    
    assert mock_repo.add_entries.called
    args = mock_repo.add_entries.call_args[0][0]
    assert len(args) == 2
    assert args[0].account_name == 'Cash'
    assert args[0].debit == Decimal("100")
    assert args[1].account_name == 'Sales'
    assert args[1].credit == Decimal("100")

def test_record_transaction_unbalanced(service):
    tx_id = uuid4()
    entries = [
        {'account': 'Cash', 'debit': Decimal("100"), 'credit': Decimal("0")},
        {'account': 'Sales', 'debit': Decimal("0"), 'credit': Decimal("50")}
    ]
    
    with pytest.raises(ValueError, match="Transaction unbalanced"):
        service.record_transaction(tx_id, entries)

def test_get_balance(service, mock_repo):
    mock_repo.get_account_balance.return_value = Decimal("500")
    assert service.get_balance("Cash") == Decimal("500")
    mock_repo.get_account_balance.assert_called_once_with("Cash")

def test_clear_transaction(service, mock_repo):
    tx_id = uuid4()
    service.clear_transaction(tx_id)
    mock_repo.delete_entries_by_transaction.assert_called_once_with(tx_id)
