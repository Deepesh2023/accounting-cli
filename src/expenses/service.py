from uuid import UUID
from decimal import Decimal
from typing import Optional
from expenses.models import Expense
from expenses.repository import ExpenseRepository
from ledger.service import LedgerService

class ExpenseService:
    def __init__(self, repository: ExpenseRepository, ledger_service: Optional[LedgerService] = None):
        self.repository = repository
        self.ledger_service = ledger_service

    def record_expense(self, expense: Expense) -> Expense:
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

    def update_expense(self, expense_id: UUID | str, expense_data: Expense) -> Expense:
        uid = UUID(expense_id) if isinstance(expense_id, str) else expense_id
        expense_data.expense_id = uid
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
