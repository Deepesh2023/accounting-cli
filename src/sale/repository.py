from uuid import UUID
from sqlmodel import Session, select
from sale.models import Sale, SaleItem
from decimal import Decimal

class SaleRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_sale(self, sale: Sale) -> Sale:
        self.session.add(sale)
        self.session.commit()
        self.session.refresh(sale)
        return sale

    def get_sale(self, sale_id: UUID) -> Sale | None:
        return self.session.get(Sale, sale_id)

    def list_sales(self) -> list[Sale]:
        stmt = select(Sale)
        return self.session.execute(stmt).scalars().all()

    def delete_sale(self, sale_id: UUID) -> bool:
        sale = self.get_sale(sale_id)
        if not sale:
            return False
        
        # Delete items first due to foreign key constraints
        self.session.delete(sale)
        self.session.commit()
        return True

    def update_sale(self, sale_data: Sale) -> Sale:
        db_sale = self.get_sale(sale_data.sale_id)
        if not db_sale:
            raise ValueError("Sale not found")
        
        # Update header fields
        db_sale.party_id = sale_data.party_id
        db_sale.total_taxable = sale_data.total_taxable
        db_sale.total_tax = sale_data.total_tax
        db_sale.grand_total = sale_data.grand_total
        db_sale.paid_amount = sale_data.paid_amount
        db_sale.balance_amount = sale_data.balance_amount
        db_sale.round_off = sale_data.round_off
        
        self.session.commit()
        self.session.refresh(db_sale)
        return db_sale
