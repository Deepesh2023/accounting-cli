from uuid import UUID, uuid4
from typing import Optional
from sqlmodel import Session, select
from src.quotation.models import Quotation, QuotationItem

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

    def update_quotation(self, quotation: Quotation) -> Quotation:
        db_quotation = self.get_quotation(quotation.quotation_id)
        if not db_quotation:
            raise ValueError("Quotation not found")
        
        db_quotation.date = quotation.date
        db_quotation.party_id = quotation.party_id
        db_quotation.total_amount = quotation.total_amount
        db_quotation.status = quotation.status
        db_quotation.notes = quotation.notes
        
        for item in list(db_quotation.items):
            self.session.delete(item)
        
        for item in quotation.items:
            new_item = QuotationItem(
                item_id=uuid4(),
                quotation_id=db_quotation.quotation_id,
                product_id=item.product_id,
                name=item.name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item.total_price
            )
            self.session.add(new_item)
        
        self.session.commit()
        self.session.refresh(db_quotation)
        return db_quotation

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
