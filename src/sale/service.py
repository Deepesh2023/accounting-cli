import uuid
from uuid import UUID
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Optional

from sale.models import Sale, SaleItem
from sale.repository import SaleRepository
from inventory.repository import InventoryRepository
from parties.repository import PartyRepository
from shared.exceptions import ProductNotFoundError, InvalidProductDataError

class SaleService:
    def __init__(self, 
                 sale_repository: SaleRepository, 
                 inventory_repository: InventoryRepository,
                 party_repository: PartyRepository):
        self.sale_repository = sale_repository
        self.inventory_repository = inventory_repository
        self.party_repository = party_repository

    def record_sale(self, 
                    items_data: list, 
                    party_id: Optional[UUID] = None, 
                    paid_amount: Decimal = Decimal("0"), 
                    round_off: bool = False,
                    tax_inclusive: bool = False) -> Sale:
        """
        items_data should be a list of dicts: 
        [{'product_id': UUID, 'quantity': int, 'discount_perc': float | None, 'discount_amt': float | None, 'tax_perc': float}]
        """
        total_taxable = Decimal("0")
        total_tax = Decimal("0")
        sale_items = []
        
        # 1. Process Row-level Calculations
        for data in items_data:
            product = self.inventory_repository.get_product(data['product_id'])
            if not product:
                raise ProductNotFoundError(f"Product {data['product_id']} not found")
            
            if product.quantity < data['quantity']:
                raise ValueError(f"Insufficient stock for {product.name}")

            gross = product.selling_price * data['quantity']
            
            # Discount Logic
            disc_amt = Decimal("0")
            if data.get('discount_perc') is not None:
                disc_amt = (gross * Decimal(str(data['discount_perc']))) / Decimal("100")
            elif data.get('discount_amt') is not None:
                disc_amt = Decimal(str(data['discount_amt']))
            
            taxable = max(Decimal("0"), gross - disc_amt)
            tax_perc = Decimal(str(data.get('tax_perc', 0)))
            
            # Tax Calculation
            if not tax_inclusive: # Exclusive
                tax_amt = taxable * (tax_perc / Decimal("100"))
            else: # Inclusive
                base = taxable / (1 + (tax_perc / Decimal("100")))
                tax_amt = taxable - base
                taxable = base
            
            row_total = taxable + tax_amt
            
            sale_items.append(SaleItem(
                sale_item_id=uuid.uuid4(),
                product_id=product.product_id,
                name=product.name,
                quantity=data['quantity'],
                price=product.selling_price,
                discount_amount=disc_amt,
                taxable_amount=taxable.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
                tax_amount=tax_amt.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
                row_total=row_total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            ))
            
            total_taxable += taxable
            total_tax += tax_amt

        grand_total = (total_taxable + total_tax).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        
        if round_off:
            grand_total = grand_total.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
            
        balance = max(Decimal("0"), grand_total - paid_amount)

        # 2. Cross-Domain Updates (Atomic within the session)
        # Update Inventory
        for item in sale_items:
            product = self.inventory_repository.get_product(item.product_id)
            product.quantity -= item.quantity
            self.inventory_repository.update_product(product)
            
        # Update Party Balance
        if party_id:
            # Credit sale increases Debtor balance
            self.party_repository.update_balance(party_id, balance)

        # 3. Save Sale
        sale = Sale(
            sale_id=uuid.uuid4(),
            date=datetime.now(),
            party_id=party_id,
            total_taxable=total_taxable.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            total_tax=total_tax.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            grand_total=grand_total,
            paid_amount=paid_amount,
            balance_amount=balance,
            round_off=round_off,
            items=sale_items
        )
        
        return self.sale_repository.add_sale(sale)

    def list_sales(self) -> list[Sale]:
        return self.sale_repository.list_sales()

    def get_sale(self, sale_id: UUID) -> Sale:
        sale = self.sale_repository.get_sale(sale_id)
        if not sale:
            raise ValueError("Sale not found")
        return sale
