import uuid
from decimal import Decimal
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, ConfigDict

from parties.service import PartyService
from parties.models import PartyType
from api.deps import get_parties_service


router = APIRouter()


class PartyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    party_id: uuid.UUID
    name: str
    party_type: PartyType
    balance: Decimal
    address: Optional[str] = None
    phone: Optional[str] = None
    state: str = ""
    gstin: Optional[str] = None


class PartyCreate(BaseModel):
    name: str
    party_type: PartyType
    balance: Decimal = Decimal("0")
    address: Optional[str] = None
    phone: Optional[str] = None
    state: str = ""
    gstin: Optional[str] = None


class PartyUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None


class BalanceAdjust(BaseModel):
    amount: Decimal


@router.get("", response_model=List[PartyResponse])
def list_parties(
    party_type: Optional[PartyType] = Query(None),
    service: PartyService = Depends(get_parties_service),
):
    return service.list_parties(party_type)


@router.get("/{party_id}", response_model=PartyResponse)
def get_party(
    party_id: uuid.UUID,
    service: PartyService = Depends(get_parties_service),
):
    try:
        return service.get_party(party_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Party not found")


@router.post("", response_model=PartyResponse, status_code=status.HTTP_201_CREATED)
def create_party(
    data: PartyCreate,
    service: PartyService = Depends(get_parties_service),
):
    try:
        return service.create_party(
            name=data.name,
            party_type=data.party_type,
            balance=data.balance,
            address=data.address,
            phone=data.phone,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{party_id}", response_model=PartyResponse)
def update_party(
    party_id: uuid.UUID,
    data: PartyUpdate,
    service: PartyService = Depends(get_parties_service),
):
    try:
        return service.update_party_info(
            party_id=party_id,
            name=data.name,
            address=data.address,
            phone=data.phone,
        )
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Party not found")


@router.delete("/{party_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_party(
    party_id: uuid.UUID,
    service: PartyService = Depends(get_parties_service),
):
    try:
        service.delete_party(party_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Party not found")


@router.post("/{party_id}/adjust-balance", response_model=PartyResponse)
def adjust_balance(
    party_id: uuid.UUID,
    data: BalanceAdjust,
    service: PartyService = Depends(get_parties_service),
):
    try:
        return service.adjust_balance(party_id, data.amount)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Party not found")
