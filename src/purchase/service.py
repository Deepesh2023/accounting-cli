import uuid
from uuid import UUID
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Optional

from purchase.models import Purchase, PurchaseItem
from purchase.repository import PurchaseRepository
from inventory.repository import InventoryRepository
from parties.repository import PartyRepository
from ledger.service import LedgerService
from shared.exceptions import ProductNotFoundError

class PurchaseService:
    def __init__(self, 
                 purchase_repository: PurchaseRepository, 
                 inventory_repository: InventoryRepository,
                 party_repository: PartyRepository,
                 ledger_service: LedgerService):
        self.purchase_repository = purchase_repository
        self.inventory_repository = inventory_repository
        self.party_repository = party_repository
        self.ledger_service = ledger_service

    def record_purchase(self, 
                        items_data: list, 
                        party_id: Optional[UUID] = None, 
                        paid_amount: Decimal = Decimal("0"), 
                        round_off: bool = False,
                        tax_inclusive: bool = False) -> Purchase:
        """
        items_data should be a list of dicts: 
        [{'product_id': UUID, 'quantity': int, 'discount_perc': float | None, 'discount_amt': float | None, 'tax_perc': float}]
        """
        total_taxable = Decimal("0")
        total_tax = Decimal("0")
        total_cgst = Decimal("0")
        total_sgst = Decimal("0")
        total_igst = Decimal("0")
        purchase_items = []
        
        # Determine if Inter-state or Intra-state
        is_interstate = False
        party = None
        if party_id:
            party = self.party_repository.get_party(party_id)
            # Hardcoded Company State for prototype: "Karnataka"
            company_state = "Karnataka"
            if party.state and party.state != company_state:
                is_interstate = True

        # 1. Process Row-level Calculations
        for data in items_data:
            product = self.inventory_repository.get_product(data['product_id'])
            if not product:
                raise ProductNotFoundError(f"Product {data['product_id']} not found")

            gross = product.selling_price * data['quantity']
            
            # Discount Logic
            disc_amt = Decimal("0")
            if data.get('discount_perc') is not None:
                disc_amt = (gross * Decimal(str(data['discount_perc']))) / Decimal("100")
            elif data.get('discount_amt') is not None:
                disc_amt = Decimal(str(data['discount_amt']))
            
            taxable = max(Decimal("0"), gross - disc_amt)
            
            # Use product's GST rate if tax_perc not provided
            tax_perc = Decimal(str(data.get('tax_perc', product.gst_rate)))
            
            # Tax Calculation
            if not tax_inclusive: # Exclusive
                tax_amt = taxable * (tax_perc / Decimal("100"))
            else: # Inclusive
                base = taxable / (1 + (tax_perc / Decimal("100")))
                tax_amt = taxable - base
                taxable = base
            
            # Split GST
            cgst, sgst, igst = Decimal("0"), Decimal("0"), Decimal("0")
            if is_interstate:
                igst = tax_amt
            else:
                cgst = tax_amt / 2
                sgst = tax_amt / 2
            
            row_total = taxable + tax_amt
            
            purchase_items.append(PurchaseItem(
                purchase_item_id=uuid.uuid4(),
                purchase_id=None, 
                product_id=product.product_id,
                name=product.name,
                quantity=data['quantity'],
                price=product.selling_price,
                discount_amount=disc_amt,
                taxable_amount=taxable.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
                tax_amount=tax_amt.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
                cgst_amount=cgst.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
                sgst_amount=sgst.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
                igst_amount=igst.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
                row_total=row_total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            ))
            
            total_taxable += taxable
            total_tax += tax_amt
            total_cgst += cgst
            total_sgst += sgst
            total_igst += igst

        grand_total = (total_taxable + total_tax).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        
        if round_off:
            grand_total = grand_total.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
            
        balance = max(Decimal("0"), grand_total - paid_amount)

        # 2. Cross-Domain Updates
        # Update Inventory (ADD stock)
        for item in purchase_items:
            product = self.inventory_repository.get_product(item.product_id)
            product.quantity += item.quantity
            self.inventory_repository.update_product(product)
            
        # Update Party Balance
        if party_id:
            self.party_repository.update_balance(party_id, balance)

        # 3. Save Purchase
        purchase = Purchase(
            purchase_id=uuid.uuid4(),
            date=datetime.now(),
            party_id=party_id,
            total_taxable=total_taxable.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            total_tax=total_tax.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            grand_total=grand_total,
            paid_amount=paid_amount,
            balance_amount=balance,
            round_off=round_off,
            items=purchase_items
        )
        
        # Assign purchase_id to items
        for item in purchase_items:
            item.purchase_id = purchase.purchase_id
            
        self.purchase_repository.add_purchase(purchase)

        # 4. Ledger Entry (Double Entry)
        entries = []
        # Basic Purchase Value (DR)
        entries.append({'account': 'Purchases', 'debit': total_taxable.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), 'credit': Decimal("0"), 'desc': f"Purchase Transaction {purchase.purchase_id}"})
        
        # Input Tax Credits (DR)
        if total_cgst > 0:
            entries.append({'account': 'Input CGST', 'debit': total_cgst.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), 'credit': Decimal("0"), 'desc': f"ITC CGST for {purchase.purchase_id}"})
        if total_sgst > 0:
            entries.append({'account': 'Input SGST', 'debit': total_sgst.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), 'credit': Decimal("0"), 'desc': f"ITC SGST for {purchase.purchase_id}"})
        if total_igst > 0:
            entries.append({'account': 'Input IGST', 'debit': total_igst.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), 'credit': Decimal("0"), 'desc': f"ITC IGST for {purchase.purchase_id}"})
        
        # Payments/Liability (CR)
        if paid_amount > 0:
            entries.append({'account': 'Cash', 'debit': Decimal("0"), 'credit': paid_amount, 'desc': f"Payment for Purchase {purchase.purchase_id}"})
        
        if balance > 0 and party:
            entries.append({'account': f"Party: {party.name}", 'debit': Decimal("0"), 'credit': balance, 'desc': f"Credit Purchase from {party.name}"})
        
        self.ledger_service.record_transaction(purchase.purchase_id, entries)

        return purchase

    def list_purchases(self) -> list[Purchase]:
        return self.purchase_repository.list_purchases()

    def get_purchase(self, purchase_id: UUID) -> Purchase:
        purchase = self.purchase_repository.get_purchase(purchase_id)
        if not purchase:
            raise ValueError("Purchase not found")
        return purchase
