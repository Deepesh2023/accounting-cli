from uuid import UUID
from typing import Optional
from sqlmodel import Session, select
from quotation.models import Quotation, QuotationItem

class QuotationRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_quotation(self, quotation: Quotation) -> Quotation:
        self.session.add(quotation)
        self.session.commit()
        self.session.refresh(quotation)
        return quotation

    def get_quotation(self, quotation_id: UUID) -> Quotation | None:
        return self.session.get(Quotation, quotation_id)

    def list_quotations(self) -> list[Quotation]:
        return self.session.exec(select(Quotation)).all()

    def delete_quotation(self, quotation_id: UUID) -> bool:
        quotation = self.get_quotation(quotation_id)
        if not quotation:
            return False
        # Delete items first
        stmt = select(QuotationItem).where(QuotationItem.quotation_id == quotation_id)
        items = self.session.execute(stmt).scalars().all()
        for item in items:
            self.session.delete(item)
        
        self.session.delete(quotation)
        self.session.commit()
        return True
