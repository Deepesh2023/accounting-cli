from sale.models import Sale, SaleItem
from shared.interfaces import SaleRepositoryProtocol, InventoryRepositoryProtocol
from datetime import datetime
import uuid

class SaleService:
    def __init__(self, sale_repository: SaleRepositoryProtocol, inventory_repository: InventoryRepositoryProtocol):
        self.sale_repository = sale_repository
        self.inventory_repository = inventory_repository

    def record_sale(self, items: list[SaleItem], customer_name: str = None) -> Sale:
        # 1. Update Inventory
        for item in items:
            product = self.inventory_repository.get_product(item.product_id)
            if product:
                product.quantity -= item.quantity
                self.inventory_repository.update_product(product)

        # 2. Record Sale
        sale = Sale(
            sale_id=uuid.uuid4(),
            date=datetime.now(),
            items=items,
            customer_name=customer_name,
        )
        self.sale_repository.add_sale(sale)
        return sale

    def list_sales(self) -> list[Sale]:
        return self.sale_repository.list_sales()

    def get_sale(self, sale_id: uuid.UUID) -> Sale:
        sale = self.sale_repository.get_sale(sale_id)
        if not sale:
            raise ValueError("Sale not found")
        return sale
