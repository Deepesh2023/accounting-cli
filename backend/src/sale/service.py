import uuid
from uuid import UUID
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from src.sale.models import Sale, SaleItem
from src.sale.repository import SaleRepository
from src.inventory.repository import InventoryRepository
from src.parties.repository import PartyRepository
from src.ledger.service import LedgerService
from src.shared.exceptions import ProductNotFoundError
from src.shared.accounts import CASH, SALES_REVENUE, OUTPUT_CGST, OUTPUT_SGST, OUTPUT_IGST
from src.shared.transaction_utils import compute_row, compute_grand_total, party_prefix

COMPANY_STATE = "Karnataka"

class SaleService:
    def __init__(self,
                 sale_repository: SaleRepository,
                 inventory_repository: InventoryRepository,
                 party_repository: PartyRepository,
                 ledger_service: LedgerService):
        self.sale_repository = sale_repository
        self.inventory_repository = inventory_repository
        self.party_repository = party_repository
        self.ledger_service = ledger_service

    def _resolve_party_and_state(self, party_id: UUID | None):
        is_interstate = False
        party = None
        if party_id:
            party = self.party_repository.get_party(party_id)
            if party.state and party.state != COMPANY_STATE:
                is_interstate = True
        return party, is_interstate

    def _process_items(self, items_data: list, is_interstate: bool, tax_inclusive: bool):
        total_taxable = Decimal("0")
        total_tax = Decimal("0")
        total_cgst = Decimal("0")
        total_sgst = Decimal("0")
        total_igst = Decimal("0")
        sale_items = []

        for data in items_data:
            product = self.inventory_repository.get_product(data['product_id'])
            if not product:
                raise ProductNotFoundError(f"Product {data['product_id']} not found")
            if product.quantity < data['quantity']:
                raise ValueError(f"Insufficient stock for {product.name}")

            raw_tax = data.get('tax_perc')
            tax_perc = product.gst_rate if raw_tax is None else Decimal(str(raw_tax))

            row = compute_row(
                price=product.selling_price,
                quantity=data['quantity'],
                gst_rate=tax_perc,
                discount_perc=data.get('discount_perc'),
                discount_amt=data.get('discount_amt'),
                is_interstate=is_interstate,
                tax_inclusive=tax_inclusive,
            )

            sale_items.append(SaleItem(
                sale_item_id=uuid.uuid4(),
                product_id=product.product_id,
                name=product.name,
                quantity=data['quantity'],
                price=product.selling_price,
                discount_amount=row['discount_amount'],
                taxable_amount=row['taxable_amount'],
                tax_amount=row['tax_amount'],
                cgst_amount=row['cgst_amount'],
                sgst_amount=row['sgst_amount'],
                igst_amount=row['igst_amount'],
                row_total=row['row_total'],
            ))

            total_taxable += row['taxable_amount']
            total_tax += row['tax_amount']
            total_cgst += row['cgst_amount']
            total_sgst += row['sgst_amount']
            total_igst += row['igst_amount']

        return sale_items, total_taxable, total_tax, total_cgst, total_sgst, total_igst

    def _update_inventory(self, sale_items: list[SaleItem], delta: int):
        for item in sale_items:
            product = self.inventory_repository.get_product(item.product_id)
            if product is None:
                raise ProductNotFoundError(f"Product {item.product_id} not found")
            product.quantity += item.quantity * delta

    def _build_ledger_entries(self, sale_id: UUID, party, paid_amount: Decimal, balance: Decimal,
                              total_taxable: Decimal, total_cgst: Decimal, total_sgst: Decimal,
                              total_igst: Decimal) -> list[dict]:
        entries = []
        if paid_amount > 0:
            entries.append({'account': CASH, 'debit': paid_amount, 'credit': Decimal("0"),
                            'desc': f"Payment for Sale {sale_id}"})
        if balance > 0 and party:
            entries.append({'account': party_prefix(party.name), 'debit': balance, 'credit': Decimal("0"),
                            'desc': f"Credit Sale to {party.name}"})
        entries.append({'account': SALES_REVENUE, 'debit': Decimal("0"), 'credit': total_taxable,
                        'desc': f"Sale Transaction {sale_id}"})
        if total_cgst > 0:
            entries.append({'account': OUTPUT_CGST, 'debit': Decimal("0"), 'credit': total_cgst,
                            'desc': f"Output CGST for {sale_id}"})
        if total_sgst > 0:
            entries.append({'account': OUTPUT_SGST, 'debit': Decimal("0"), 'credit': total_sgst,
                            'desc': f"Output SGST for {sale_id}"})
        if total_igst > 0:
            entries.append({'account': OUTPUT_IGST, 'debit': Decimal("0"), 'credit': total_igst,
                            'desc': f"Output IGST for {sale_id}"})
        return entries

    def record_sale(self,
                     items_data: list,
                     party_id: UUID | None = None,
                     paid_amount: Decimal = Decimal("0"),
                     round_off: bool = False,
                     tax_inclusive: bool = False) -> Sale:
        party, is_interstate = self._resolve_party_and_state(party_id)
        sale_items, total_taxable, total_tax, total_cgst, total_sgst, total_igst = self._process_items(
            items_data, is_interstate, tax_inclusive)

        grand_total = compute_grand_total(total_taxable, total_tax, round_off)
        balance = max(Decimal("0"), grand_total - paid_amount)

        self._update_inventory(sale_items, -1)

        if party_id:
            self.party_repository.update_balance(party_id, balance)

        sale = Sale(
            sale_id=uuid.uuid4(),
            date=datetime.now(),
            party_id=party_id,
            total_taxable=total_taxable,
            total_tax=total_tax,
            grand_total=grand_total,
            paid_amount=paid_amount,
            balance_amount=balance,
            round_off=round_off,
            items=sale_items,
        )
        for item in sale_items:
            item.sale_id = sale.sale_id

        self.sale_repository.add_sale(sale, commit=False)

        entries = self._build_ledger_entries(sale.sale_id, party, paid_amount, balance,
                                              total_taxable, total_cgst, total_sgst, total_igst)
        self.ledger_service.record_transaction(sale.sale_id, entries)
        return sale

    def record_payment(self, sale_id: UUID, amount: Decimal) -> Sale:
        sale = self.get_sale(sale_id)
        if amount > sale.balance_amount:
            raise ValueError(f"Payment amount {amount} exceeds balance {sale.balance_amount}")

        sale.paid_amount += amount
        sale.balance_amount -= amount

        if sale.party_id:
            self.party_repository.update_balance(sale.party_id, sale.balance_amount, commit=False)

        self.sale_repository.update_sale(sale, commit=False)

        party = self.party_repository.get_party(sale.party_id) if sale.party_id else None
        entries = [
            {'account': party_prefix(party.name) if party else "Unknown Party", 'debit': Decimal("0"),
             'credit': amount, 'desc': f"Payment received for Sale {sale_id}"},
            {'account': CASH, 'debit': amount, 'credit': Decimal("0"),
             'desc': f"Payment received for Sale {sale_id}"},
        ]
        self.ledger_service.record_transaction(uuid.uuid4(), entries)
        return sale

    def list_sales(self) -> list[Sale]:
        return self.sale_repository.list_sales()

    def get_sale(self, sale_id: UUID) -> Sale:
        sale = self.sale_repository.get_sale(sale_id)
        if not sale:
            raise ValueError("Sale not found")
        return sale

    def delete_sale(self, sale_id: UUID) -> None:
        sale = self.get_sale(sale_id)
        self._update_inventory(sale.items, 1)
        if sale.party_id:
            self.party_repository.update_balance(sale.party_id, -sale.balance_amount, commit=False)
        self.ledger_service.clear_transaction(sale.sale_id, commit=False)
        self.sale_repository.delete_sale(sale_id)

    def update_sale(self,
                    sale_id: UUID,
                    items_data: list,
                    party_id: UUID | None = None,
                    paid_amount: Decimal = Decimal("0"),
                    round_off: bool = False,
                    tax_inclusive: bool = False) -> Sale:
        existing = self.get_sale(sale_id)

        self._update_inventory(existing.items, 1)
        if existing.party_id:
            self.party_repository.update_balance(existing.party_id, -existing.balance_amount, commit=False)
        self.ledger_service.clear_transaction(sale_id, commit=False)

        party, is_interstate = self._resolve_party_and_state(party_id)
        sale_items, total_taxable, total_tax, total_cgst, total_sgst, total_igst = self._process_items(
            items_data, is_interstate, tax_inclusive)

        grand_total = compute_grand_total(total_taxable, total_tax, round_off)
        balance = max(Decimal("0"), grand_total - paid_amount)

        self._update_inventory(sale_items, -1)
        if party_id:
            self.party_repository.update_balance(party_id, balance, commit=False)

        for item in sale_items:
            item.sale_id = sale_id
        self.sale_repository.replace_items(sale_id, sale_items, commit=False)

        existing.party_id = party_id
        existing.total_taxable = total_taxable
        existing.total_tax = total_tax
        existing.grand_total = grand_total
        existing.paid_amount = paid_amount
        existing.balance_amount = balance
        existing.round_off = round_off
        self.sale_repository.update_sale(existing, commit=False)

        entries = self._build_ledger_entries(sale_id, party, paid_amount, balance,
                                              total_taxable, total_cgst, total_sgst, total_igst)
        self.ledger_service.record_transaction(sale_id, entries)
        return self.sale_repository.get_sale(sale_id)
