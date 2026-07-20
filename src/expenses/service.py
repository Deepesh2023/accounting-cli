from expenses.models import Expense
from expenses.repository import ExpenseRepository

class ExpenseService:
    def __init__(self, repository: ExpenseRepository):
        self.repository = repository

    def record_expense(self, expense: Expense) -> Expense:
        # In a real app, this would also trigger a ledger entry
        return self.repository.add_expense(expense)

    def get_all_expenses(self, category: str | None = None) -> list[Expense]:
        return self.repository.list_expenses(category)

    def get_expense_by_id(self, expense_id: UUID | str) -> Expense | None:
        uid = UUID(expense_id) if isinstance(expense_id, str) else expense_id
        return self.repository.get_expense(uid)

    def remove_expense(self, expense_id: UUID | str) -> bool:
        uid = UUID(expense_id) if isinstance(expense_id, str) else expense_id
        return self.repository.delete_expense(uid)
