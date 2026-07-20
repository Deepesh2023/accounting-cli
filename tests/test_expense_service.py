import pytest
from decimal import Decimal
from datetime import datetime
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
