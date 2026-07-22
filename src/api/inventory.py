import uuid
from decimal import Decimal
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict

from inventory.service import InventoryService
from shared.exceptions import ProductNotFoundError, InvalidProductDataError
from api.deps import get_inventory_service


router = APIRouter()


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: uuid.UUID
    name: str
    selling_price: Decimal
    quantity: int
    gst_rate: Decimal
    hsn_code: str
    archived: bool


class ProductCreate(BaseModel):
    name: str
    selling_price: Decimal
    quantity: int
    gst_rate: Decimal = Decimal("0")
    hsn_code: str = ""


@router.get("", response_model=List[ProductResponse])
def list_products(
    show_archived: bool = False,
    service: InventoryService = Depends(get_inventory_service),
):
    return service.list_products(show_archived=show_archived)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: uuid.UUID,
    service: InventoryService = Depends(get_inventory_service),
):
    try:
        return service.get_product(product_id)
    except ProductNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    data: ProductCreate,
    service: InventoryService = Depends(get_inventory_service),
):
    try:
        return service.add_product(
            name=data.name,
            selling_price=data.selling_price,
            quantity=data.quantity,
            gst_rate=data.gst_rate,
            hsn_code=data.hsn_code,
        )
    except InvalidProductDataError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: uuid.UUID,
    data: ProductCreate,
    service: InventoryService = Depends(get_inventory_service),
):
    from inventory.models import Product
    try:
        existing = service.get_product(product_id)
    except ProductNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    updated = Product(
        product_id=product_id,
        name=data.name,
        selling_price=data.selling_price,
        quantity=data.quantity,
        gst_rate=data.gst_rate,
        hsn_code=data.hsn_code,
    )
    service.update_product(updated)
    return service.get_product(product_id)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: uuid.UUID,
    service: InventoryService = Depends(get_inventory_service),
):
    result = service.delete_product(product_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
