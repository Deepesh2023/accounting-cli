import pytest
from uuid import uuid4
from decimal import Decimal
from datetime import datetime
from unittest.mock import Mock
from src.expenses.repository import ExpenseRepository
from src.expenses.service import ExpenseService

def test_expense_lifecycle(session):
    # Arrange
    repo = ExpenseRepository(session)
    service = ExpenseService(repo)
    
    # Act - Record
    recorded = service.record_expense("Utilities", Decimal("500.00"), paid_by="Cash", notes="Electricity bill for June")
    assert recorded.expense_id is not None
    assert recorded.category == "Utilities"
    
    # Act - List
    expenses = service.get_all_expenses()
    assert len(expenses) == 1
    assert expenses[0].amount == Decimal("500.00")
    
    # Act - Retrieve
    retrieved = service.get_expense_by_id(recorded.expense_id)
    assert retrieved is not None
    assert retrieved.notes == "Electricity bill for June"
    
    # Act - Delete
    success = service.remove_expense(recorded.expense_id)
    assert success is True
    assert len(service.get_all_expenses()) == 0

def test_expense_category_filter(session):
    repo = ExpenseRepository(session)
    service = ExpenseService(repo)

    service.record_expense("Rent", Decimal("10000"), paid_by="Bank")
    service.record_expense("Food", Decimal("200"), paid_by="Cash")
    
    rent_expenses = service.get_all_expenses(category="Rent")
    assert len(rent_expenses) == 1
    assert rent_expenses[0].category == "Rent"

def test_expense_with_ledger_integration(session):
    repo = ExpenseRepository(session)
    mock_ledger = Mock()
    service = ExpenseService(repo, ledger_service=mock_ledger)

    recorded = service.record_expense("Rent", Decimal("10000"), paid_by="Bank", notes="Office rent")
    assert recorded.expense_id is not None
    
    assert mock_ledger.record_transaction.called
    args = mock_ledger.record_transaction.call_args[0]
    assert args[0] == recorded.expense_id
    entries = args[1]
    assert len(entries) == 2
    assert entries[0]['account'] == "Rent Expense"
    assert entries[0]['debit'] == Decimal("10000")
    assert entries[1]['account'] == "Bank"
    assert entries[1]['credit'] == Decimal("10000")

def test_update_expense(session):
    repo = ExpenseRepository(session)
    service = ExpenseService(repo)

    recorded = service.record_expense("Rent", Decimal("5000"), paid_by="Cash")

    updated = service.update_expense(recorded.expense_id, paid_by="Bank", amount=Decimal("5500"), notes="Updated rent")
    assert updated.paid_by == "Bank"
    assert updated.amount == Decimal("5500")
    assert updated.notes == "Updated rent"
    
    retrieved = service.get_expense_by_id(recorded.expense_id)
    assert retrieved.paid_by == "Bank"
    assert retrieved.amount == Decimal("5500")

def test_remove_expense_with_ledger(session):
    repo = ExpenseRepository(session)
    mock_ledger = Mock()
    service = ExpenseService(repo, ledger_service=mock_ledger)

    recorded = service.record_expense("Travel", Decimal("2000"), paid_by="Cash")
    
    assert mock_ledger.record_transaction.called
    mock_ledger.reset_mock()
    
    service.remove_expense(recorded.expense_id)
    
    assert mock_ledger.clear_transaction.called
    mock_ledger.clear_transaction.assert_called_once_with(recorded.expense_id)
    assert service.get_expense_by_id(recorded.expense_id) is None
