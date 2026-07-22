import uuid
from uuid import UUID
from decimal import Decimal
from typing import Optional
from datetime import datetime
from expenses.models import Expense
from expenses.repository import ExpenseRepository
from ledger.service import LedgerService

class ExpenseService:
    def __init__(self, repository: ExpenseRepository, ledger_service: Optional[LedgerService] = None):
        self.repository = repository
        self.ledger_service = ledger_service

    def record_expense(self, category: str, amount: Decimal, paid_by: str = "Cash", notes: str | None = None) -> Expense:
        expense = Expense(
            expense_id=uuid.uuid4(),
            date=datetime.now(),
            category=category,
            paid_by=paid_by,
            amount=amount,
            notes=notes,
        )
        recorded = self.repository.add_expense(expense)
        if self.ledger_service:
            entries = [
                {'account': f"{expense.category} Expense", 'debit': expense.amount, 'credit': Decimal("0"), 'desc': expense.notes or f"Expense: {expense.category}"},
                {'account': expense.paid_by, 'debit': Decimal("0"), 'credit': expense.amount, 'desc': f"Payment for {expense.category}"}
            ]
            self.ledger_service.record_transaction(recorded.expense_id, entries)
        return recorded

    def get_all_expenses(self, category: str | None = None) -> list[Expense]:
        return self.repository.list_expenses(category)

    def get_expense_by_id(self, expense_id: UUID | str) -> Expense | None:
        uid = UUID(expense_id) if isinstance(expense_id, str) else expense_id
        return self.repository.get_expense(uid)

    def update_expense(self, expense_id: UUID | str, category: str | None = None, paid_by: str | None = None, amount: Decimal | None = None, notes: str | None = None) -> Expense:
        uid = UUID(expense_id) if isinstance(expense_id, str) else expense_id
        existing = self.get_expense_by_id(uid)
        if not existing:
            raise ValueError("Expense not found")

        expense_data = Expense(
            expense_id=uid,
            date=existing.date,
            category=category if category is not None else existing.category,
            paid_by=paid_by if paid_by is not None else existing.paid_by,
            amount=amount if amount is not None else existing.amount,
            notes=notes if notes is not None else existing.notes,
        )
        if self.ledger_service:
            self.ledger_service.clear_transaction(uid)
        updated = self.repository.update_expense(expense_data)
        if self.ledger_service:
            entries = [
                {'account': f"{expense_data.category} Expense", 'debit': expense_data.amount, 'credit': Decimal("0"), 'desc': expense_data.notes or f"Expense: {expense_data.category}"},
                {'account': expense_data.paid_by, 'debit': Decimal("0"), 'credit': expense_data.amount, 'desc': f"Payment for {expense_data.category}"}
            ]
            self.ledger_service.record_transaction(uid, entries)
        return updated

    def remove_expense(self, expense_id: UUID | str) -> bool:
        uid = UUID(expense_id) if isinstance(expense_id, str) else expense_id
        if self.ledger_service:
            self.ledger_service.clear_transaction(uid)
        return self.repository.delete_expense(uid)
