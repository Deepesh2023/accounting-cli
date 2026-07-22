import uuid
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict

from company.models import Company
from company.service import CompanyService
from api.deps import get_company_service


router = APIRouter()


class CompanyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    company_id: uuid.UUID
    name: str
    business_type: Optional[str] = None
    category: Optional[str] = None
    beginning_date: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    logo_path: Optional[str] = None
    qr_path: Optional[str] = None


class CompanyUpdate(BaseModel):
    name: str
    business_type: Optional[str] = None
    category: Optional[str] = None
    beginning_date: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    logo_path: Optional[str] = None
    qr_path: Optional[str] = None


@router.get("", response_model=CompanyResponse)
def get_profile(
    service: CompanyService = Depends(get_company_service),
):
    profile = service.get_profile()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company profile not found")
    return profile


@router.put("", response_model=CompanyResponse)
def upsert_profile(
    data: CompanyUpdate,
    service: CompanyService = Depends(get_company_service),
):
    company = Company(**data.model_dump())
    try:
        return service.update_profile(company)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
