import uuid
from decimal import Decimal
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict

from purchase.service import PurchaseService
from shared.exceptions import ProductNotFoundError
from api.deps import get_purchase_service


router = APIRouter()


class PurchaseItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    purchase_item_id: uuid.UUID
    purchase_id: uuid.UUID
    product_id: uuid.UUID
    name: str
    quantity: int
    price: Decimal
    discount_amount: Decimal
    taxable_amount: Decimal
    tax_amount: Decimal
    cgst_amount: Decimal
    sgst_amount: Decimal
    igst_amount: Decimal
    row_total: Decimal


class PurchaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    purchase_id: uuid.UUID
    date: datetime
    party_id: Optional[uuid.UUID] = None
    total_taxable: Decimal
    total_tax: Decimal
    grand_total: Decimal
    paid_amount: Decimal
    balance_amount: Decimal
    due_date: Optional[datetime] = None
    round_off: bool
    items: List[PurchaseItemResponse] = []


class PurchaseItemInput(BaseModel):
    product_id: uuid.UUID
    quantity: int
    discount_perc: Optional[Decimal] = None
    discount_amt: Optional[Decimal] = None
    tax_perc: Optional[Decimal] = None


class PurchaseCreate(BaseModel):
    items_data: List[PurchaseItemInput]
    party_id: Optional[uuid.UUID] = None
    paid_amount: Decimal = Decimal("0")
    round_off: bool = False
    tax_inclusive: bool = False


class PaymentCreate(BaseModel):
    amount: Decimal


@router.get("", response_model=List[PurchaseResponse])
def list_purchases(
    service: PurchaseService = Depends(get_purchase_service),
):
    return service.list_purchases()


@router.get("/{purchase_id}", response_model=PurchaseResponse)
def get_purchase(
    purchase_id: uuid.UUID,
    service: PurchaseService = Depends(get_purchase_service),
):
    try:
        return service.get_purchase(purchase_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase not found")


@router.post("", response_model=PurchaseResponse, status_code=status.HTTP_201_CREATED)
def create_purchase(
    data: PurchaseCreate,
    service: PurchaseService = Depends(get_purchase_service),
):
    try:
        items = [item.model_dump() for item in data.items_data]
        return service.record_purchase(
            items_data=items,
            party_id=data.party_id,
            paid_amount=data.paid_amount,
            round_off=data.round_off,
            tax_inclusive=data.tax_inclusive,
        )
    except ProductNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{purchase_id}", response_model=PurchaseResponse)
def update_purchase(
    purchase_id: uuid.UUID,
    data: PurchaseCreate,
    service: PurchaseService = Depends(get_purchase_service),
):
    try:
        items = [item.model_dump() for item in data.items_data]
        return service.update_purchase(
            purchase_id=purchase_id,
            items_data=items,
            party_id=data.party_id,
            paid_amount=data.paid_amount,
            round_off=data.round_off,
            tax_inclusive=data.tax_inclusive,
        )
    except ProductNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{purchase_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_purchase(
    purchase_id: uuid.UUID,
    service: PurchaseService = Depends(get_purchase_service),
):
    try:
        service.delete_purchase(purchase_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase not found")


@router.post("/{purchase_id}/payment", response_model=PurchaseResponse)
def record_payment(
    purchase_id: uuid.UUID,
    data: PaymentCreate,
    service: PurchaseService = Depends(get_purchase_service),
):
    try:
        return service.record_payment(purchase_id, data.amount)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
