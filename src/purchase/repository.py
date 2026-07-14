from uuid import UUID
from sqlmodel import Session, select
from purchase.models import Purchase, PurchaseItem
from decimal import Decimal

class PurchaseRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_purchase(self, purchase: Purchase) -> Purchase:
        self.session.add(purchase)
        self.session.commit()
        self.session.refresh(purchase)
        return purchase

    def get_purchase(self, purchase_id: UUID) -> Purchase | None:
        return self.session.get(Purchase, purchase_id)

    def list_purchases(self) -> list[Purchase]:
        stmt = select(Purchase)
        return self.session.execute(stmt).scalars().all()

    def delete_purchase(self, purchase_id: UUID) -> bool:
        purchase = self.get_purchase(purchase_id)
        if not purchase:
            return False
        
        self.session.delete(purchase)
        self.session.commit()
        return True

    def update_purchase(self, purchase_data: Purchase) -> Purchase:
        db_purchase = self.get_purchase(purchase_data.purchase_id)
        if not db_purchase:
            raise ValueError("Purchase not found")
        
        db_purchase.party_id = purchase_data.party_id
        db_purchase.total_taxable = purchase_data.total_taxable
        db_purchase.total_tax = purchase_data.total_tax
        db_purchase.grand_total = purchase_data.grand_total
        db_purchase.paid_amount = purchase_data.paid_amount
        db_purchase.balance_amount = purchase_data.balance_amount
        db_purchase.round_off = purchase_data.round_off
        
        self.session.commit()
        self.session.refresh(db_purchase)
        return db_purchase
