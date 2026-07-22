import uuid
from decimal import Decimal
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, ConfigDict

from expenses.service import ExpenseService
from expenses.models import Expense
from api.deps import get_expense_service


router = APIRouter()


class ExpenseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    expense_id: uuid.UUID
    date: datetime
    category: str
    paid_by: str
    amount: Decimal
    notes: Optional[str] = None


class ExpenseCreate(BaseModel):
    category: str
    paid_by: str = "Cash"
    amount: Decimal
    notes: Optional[str] = None


@router.get("", response_model=List[ExpenseResponse])
def list_expenses(
    category: Optional[str] = Query(None),
    service: ExpenseService = Depends(get_expense_service),
):
    return service.get_all_expenses(category)


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: uuid.UUID,
    service: ExpenseService = Depends(get_expense_service),
):
    expense = service.get_expense_by_id(expense_id)
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return expense


@router.post("", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    data: ExpenseCreate,
    service: ExpenseService = Depends(get_expense_service),
):
    expense = Expense(
        expense_id=uuid.uuid4(),
        category=data.category,
        paid_by=data.paid_by,
        amount=data.amount,
        notes=data.notes,
    )
    return service.record_expense(expense)


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: uuid.UUID,
    data: ExpenseCreate,
    service: ExpenseService = Depends(get_expense_service),
):
    expense = Expense(
        expense_id=expense_id,
        category=data.category,
        paid_by=data.paid_by,
        amount=data.amount,
        notes=data.notes,
    )
    try:
        updated = service.update_expense(expense_id, expense)
        return updated
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: uuid.UUID,
    service: ExpenseService = Depends(get_expense_service),
):
    result = service.remove_expense(expense_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
