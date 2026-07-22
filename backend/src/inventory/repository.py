from uuid import UUID
from sqlmodel import Session, select, or_
from inventory.models import Product
from shared.exceptions import ProductNotFoundError

class InventoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_product(self, product: Product):
        self.session.add(product)
        self.session.commit()

    def get_product(self, product_id: UUID) -> Product | None:
        return self.session.get(Product, product_id)

    def list_products(self) -> list[Product]:
        return self.session.execute(select(Product)).scalars().all()

    def search_products(self, query: str) -> list[Product]:
        conditions = [Product.name.ilike(f"%{query}%")]
        try:
            uuid_val = UUID(query.strip())
            conditions.append(Product.product_id == uuid_val)
        except ValueError:
            pass
        stmt = select(Product).where(or_(*conditions))
        return self.session.execute(stmt).scalars().all()

    def change_visibility(self, product_id: UUID) -> Product | None:
        product = self.get_product(product_id)
        if product:
            product.archived = not product.archived
            self.session.commit()
        return product

    def update_product(self, updated_product: Product):
        product = self.get_product(product_id=updated_product.product_id)
        if not product:
            raise ProductNotFoundError("Cannot find product.")

        product.name = updated_product.name
        product.selling_price = updated_product.selling_price
        product.quantity = updated_product.quantity
        product.gst_rate = updated_product.gst_rate
        product.hsn_code = updated_product.hsn_code
        product.archived = updated_product.archived
        self.session.commit()

    def delete_product(self, product_id: UUID) -> bool:
        product = self.get_product(product_id)
        if not product:
            return False
        self.session.delete(product)
        self.session.commit()
        return True

