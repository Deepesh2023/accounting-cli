import pytest
from uuid import uuid4
from decimal import Decimal
from datetime import datetime
from unittest.mock import Mock
from expenses.models import Expense
from expenses.repository import ExpenseRepository
from expenses.service import ExpenseService

def test_expense_lifecycle(session):
    # Arrange
    repo = ExpenseRepository(session)
    service = ExpenseService(repo)
    
    expense_data = Expense(
        category="Utilities",
        paid_by="Cash",
        amount=Decimal("500.00"),
        notes="Electricity bill for June"
    )
    
    # Act - Record
    recorded = service.record_expense(expense_data)
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
    
    service.record_expense(Expense(category="Rent", paid_by="Bank", amount=Decimal("10000")))
    service.record_expense(Expense(category="Food", paid_by="Cash", amount=Decimal("200")))
    
    rent_expenses = service.get_all_expenses(category="Rent")
    assert len(rent_expenses) == 1
    assert rent_expenses[0].category == "Rent"

def test_expense_with_ledger_integration(session):
    repo = ExpenseRepository(session)
    mock_ledger = Mock()
    service = ExpenseService(repo, ledger_service=mock_ledger)
    
    expense = Expense(
        category="Rent",
        paid_by="Bank",
        amount=Decimal("10000"),
        notes="Office rent"
    )
    
    recorded = service.record_expense(expense)
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
    
    expense = Expense(category="Rent", paid_by="Cash", amount=Decimal("5000"))
    recorded = service.record_expense(expense)
    
    updated_data = Expense(
        expense_id=recorded.expense_id,
        category="Rent",
        paid_by="Bank",
        amount=Decimal("5500"),
        notes="Updated rent"
    )
    
    updated = service.update_expense(recorded.expense_id, updated_data)
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
    
    expense = Expense(category="Travel", paid_by="Cash", amount=Decimal("2000"))
    recorded = service.record_expense(expense)
    
    assert mock_ledger.record_transaction.called
    mock_ledger.reset_mock()
    
    service.remove_expense(recorded.expense_id)
    
    assert mock_ledger.clear_transaction.called
    mock_ledger.clear_transaction.assert_called_once_with(recorded.expense_id)
    assert service.get_expense_by_id(recorded.expense_id) is None
