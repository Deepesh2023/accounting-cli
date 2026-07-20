from uuid import UUID
from typing import Optional
from sqlmodel import Session, select
from expenses.models import Expense

class ExpenseRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_expense(self, expense: Expense) -> Expense:
        self.session.add(expense)
        self.session.commit()
        self.session.refresh(expense)
        return expense

    def get_expense(self, expense_id: UUID) -> Expense | None:
        return self.session.get(Expense, expense_id)

    def list_expenses(self, category: Optional[str] = None) -> list[Expense]:
        stmt = select(Expense)
        if category:
            stmt = stmt.where(Expense.category == category)
        return self.session.execute(stmt).scalars().all()

    def delete_expense(self, expense_id: UUID) -> bool:
        expense = self.get_expense(expense_id)
        if not expense:
            return False
        self.session.delete(expense)
        self.session.commit()
        return True
