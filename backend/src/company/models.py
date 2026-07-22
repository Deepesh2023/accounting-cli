from uuid import UUID, uuid4
from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field

class Company(SQLModel, table=True):
    company_id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(nullable=False)
    business_type: Optional[str] = Field(default=None)
    category: Optional[str] = Field(default=None)
    beginning_date: Optional[date] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    address: Optional[str] = Field(default=None)
    logo_path: Optional[str] = Field(default=None)
    qr_path: Optional[str] = Field(default=None)
