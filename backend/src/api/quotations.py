import uuid
from decimal import Decimal
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict

from src.quotation.service import QuotationService
from src.quotation.models import Quotation, QuotationItem
from src.api.deps import get_quotation_service


router = APIRouter()


class QuotationItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    item_id: uuid.UUID
    quotation_id: uuid.UUID
    product_id: uuid.UUID
    name: str
    quantity: int
    unit_price: Decimal
    total_price: Decimal


class QuotationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    quotation_id: uuid.UUID
    date: datetime
    party_id: Optional[uuid.UUID] = None
    total_amount: Decimal
    status: str = "Draft"
    notes: Optional[str] = None
    items: List[QuotationItemResponse] = []


class QuotationItemInput(BaseModel):
    product_id: uuid.UUID
    name: str
    quantity: int
    unit_price: Decimal


class QuotationCreate(BaseModel):
    party_id: Optional[uuid.UUID] = None
    status: str = "Draft"
    notes: Optional[str] = None
    items: List[QuotationItemInput]


@router.get("", response_model=List[QuotationResponse])
def list_quotations(
    service: QuotationService = Depends(get_quotation_service),
):
    return service.get_all_quotations()


@router.get("/{quotation_id}", response_model=QuotationResponse)
def get_quotation(
    quotation_id: uuid.UUID,
    service: QuotationService = Depends(get_quotation_service),
):
    q = service.get_quotation_by_id(quotation_id)
    if not q:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quotation not found")
    return q


@router.post("", response_model=QuotationResponse, status_code=status.HTTP_201_CREATED)
def create_quotation(
    data: QuotationCreate,
    service: QuotationService = Depends(get_quotation_service),
):
    total = sum(item.unit_price * item.quantity for item in data.items)
    items = [
        QuotationItem(
            item_id=uuid.uuid4(),
            product_id=item.product_id,
            name=item.name,
            quantity=item.quantity,
            unit_price=item.unit_price,
            total_price=item.unit_price * item.quantity,
        )
        for item in data.items
    ]
    quotation = Quotation(
        quotation_id=uuid.uuid4(),
        party_id=data.party_id,
        total_amount=total,
        status=data.status,
        notes=data.notes,
        items=items,
    )
    return service.create_quotation(quotation)


@router.put("/{quotation_id}", response_model=QuotationResponse)
def update_quotation(
    quotation_id: uuid.UUID,
    data: QuotationCreate,
    service: QuotationService = Depends(get_quotation_service),
):
    total = sum(item.unit_price * item.quantity for item in data.items)
    items = [
        QuotationItem(
            item_id=uuid.uuid4(),
            product_id=item.product_id,
            name=item.name,
            quantity=item.quantity,
            unit_price=item.unit_price,
            total_price=item.unit_price * item.quantity,
        )
        for item in data.items
    ]
    quotation = Quotation(
        quotation_id=quotation_id,
        party_id=data.party_id,
        total_amount=total,
        status=data.status,
        notes=data.notes,
        items=items,
    )
    try:
        return service.update_quotation(quotation_id, quotation)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quotation not found")


@router.delete("/{quotation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quotation(
    quotation_id: uuid.UUID,
    service: QuotationService = Depends(get_quotation_service),
):
    result = service.remove_quotation(quotation_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quotation not found")
