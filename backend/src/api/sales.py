import uuid
from decimal import Decimal
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict

from src.sale.service import SaleService
from src.sale.models import Sale
from src.shared.exceptions import ProductNotFoundError
from src.api.deps import get_sale_service


router = APIRouter()


class SaleItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sale_item_id: uuid.UUID
    sale_id: uuid.UUID
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


class SaleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sale_id: uuid.UUID
    date: datetime
    party_id: Optional[uuid.UUID] = None
    total_taxable: Decimal
    total_tax: Decimal
    grand_total: Decimal
    paid_amount: Decimal
    balance_amount: Decimal
    due_date: Optional[datetime] = None
    round_off: bool
    items: List[SaleItemResponse] = []


class SaleItemInput(BaseModel):
    product_id: uuid.UUID
    quantity: int
    discount_perc: Optional[Decimal] = None
    discount_amt: Optional[Decimal] = None
    tax_perc: Optional[Decimal] = None


class SaleCreate(BaseModel):
    items_data: List[SaleItemInput]
    party_id: Optional[uuid.UUID] = None
    paid_amount: Decimal = Decimal("0")
    round_off: bool = False
    tax_inclusive: bool = False


class PaymentCreate(BaseModel):
    amount: Decimal


@router.get("", response_model=List[SaleResponse])
def list_sales(
    service: SaleService = Depends(get_sale_service),
):
    return service.list_sales()


@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale(
    sale_id: uuid.UUID,
    service: SaleService = Depends(get_sale_service),
):
    try:
        return service.get_sale(sale_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")


@router.post("", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def create_sale(
    data: SaleCreate,
    service: SaleService = Depends(get_sale_service),
):
    try:
        items = [item.model_dump() for item in data.items_data]
        return service.record_sale(
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


@router.put("/{sale_id}", response_model=SaleResponse)
def update_sale(
    sale_id: uuid.UUID,
    data: SaleCreate,
    service: SaleService = Depends(get_sale_service),
):
    try:
        items = [item.model_dump() for item in data.items_data]
        return service.update_sale(
            sale_id=sale_id,
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


@router.delete("/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sale(
    sale_id: uuid.UUID,
    service: SaleService = Depends(get_sale_service),
):
    try:
        service.delete_sale(sale_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")


@router.post("/{sale_id}/payment", response_model=SaleResponse)
def record_payment(
    sale_id: uuid.UUID,
    data: PaymentCreate,
    service: SaleService = Depends(get_sale_service),
):
    try:
        return service.record_payment(sale_id, data.amount)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
