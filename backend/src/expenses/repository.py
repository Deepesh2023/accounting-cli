from uuid import UUID
from typing import Optional
from sqlmodel import Session, select
from src.expenses.models import Expense

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

    def update_expense(self, expense: Expense) -> Expense:
        db_expense = self.get_expense(expense.expense_id)
        if not db_expense:
            raise ValueError("Expense not found")
        db_expense.date = expense.date
        db_expense.category = expense.category
        db_expense.paid_by = expense.paid_by
        db_expense.amount = expense.amount
        db_expense.notes = expense.notes
        self.session.commit()
        self.session.refresh(db_expense)
        return db_expense

    def delete_expense(self, expense_id: UUID) -> bool:
        expense = self.get_expense(expense_id)
        if not expense:
            return False
        self.session.delete(expense)
        self.session.commit()
        return True
