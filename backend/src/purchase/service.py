import uuid
from uuid import UUID
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from purchase.models import Purchase, PurchaseItem
from purchase.repository import PurchaseRepository
from inventory.repository import InventoryRepository
from parties.repository import PartyRepository
from ledger.service import LedgerService
from shared.exceptions import ProductNotFoundError
from shared.accounts import CASH, PURCHASES, INPUT_CGST, INPUT_SGST, INPUT_IGST
from shared.transaction_utils import compute_row, compute_grand_total, party_prefix

COMPANY_STATE = "Karnataka"

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
        purchase_items = []

        for data in items_data:
            product = self.inventory_repository.get_product(data['product_id'])
            if not product:
                raise ProductNotFoundError(f"Product {data['product_id']} not found")

            price = data.get('price', product.selling_price)
            raw_tax = data.get('tax_perc')
            tax_perc = product.gst_rate if raw_tax is None else Decimal(str(raw_tax))

            row = compute_row(
                price=price,
                quantity=data['quantity'],
                gst_rate=tax_perc,
                discount_perc=data.get('discount_perc'),
                discount_amt=data.get('discount_amt'),
                is_interstate=is_interstate,
                tax_inclusive=tax_inclusive,
            )

            purchase_items.append(PurchaseItem(
                purchase_item_id=uuid.uuid4(),
                product_id=product.product_id,
                name=product.name,
                quantity=data['quantity'],
                price=price,
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

        return purchase_items, total_taxable, total_tax, total_cgst, total_sgst, total_igst

    def _update_inventory(self, purchase_items: list[PurchaseItem], delta: int):
        for item in purchase_items:
            product = self.inventory_repository.get_product(item.product_id)
            product.quantity += item.quantity * delta
            self.inventory_repository.update_product(product)

    def _build_ledger_entries(self, purchase_id: UUID, party, paid_amount: Decimal, balance: Decimal,
                              total_taxable: Decimal, total_cgst: Decimal, total_sgst: Decimal,
                              total_igst: Decimal) -> list[dict]:
        entries = []
        entries.append({'account': PURCHASES, 'debit': total_taxable, 'credit': Decimal("0"),
                        'desc': f"Purchase Transaction {purchase_id}"})
        if total_cgst > 0:
            entries.append({'account': INPUT_CGST, 'debit': total_cgst, 'credit': Decimal("0"),
                            'desc': f"ITC CGST for {purchase_id}"})
        if total_sgst > 0:
            entries.append({'account': INPUT_SGST, 'debit': total_sgst, 'credit': Decimal("0"),
                            'desc': f"ITC SGST for {purchase_id}"})
        if total_igst > 0:
            entries.append({'account': INPUT_IGST, 'debit': total_igst, 'credit': Decimal("0"),
                            'desc': f"ITC IGST for {purchase_id}"})
        if paid_amount > 0:
            entries.append({'account': CASH, 'debit': Decimal("0"), 'credit': paid_amount,
                            'desc': f"Payment for Purchase {purchase_id}"})
        if balance > 0 and party:
            entries.append({'account': party_prefix(party.name), 'debit': Decimal("0"), 'credit': balance,
                            'desc': f"Credit Purchase from {party.name}"})
        return entries

    def record_purchase(self,
                        items_data: list,
                        party_id: UUID | None = None,
                        paid_amount: Decimal = Decimal("0"),
                        round_off: bool = False,
                        tax_inclusive: bool = False) -> Purchase:
        party, is_interstate = self._resolve_party_and_state(party_id)
        purchase_items, total_taxable, total_tax, total_cgst, total_sgst, total_igst = self._process_items(
            items_data, is_interstate, tax_inclusive)

        grand_total = compute_grand_total(total_taxable, total_tax, round_off)
        balance = max(Decimal("0"), grand_total - paid_amount)

        self._update_inventory(purchase_items, 1)

        if party_id:
            self.party_repository.update_balance(party_id, balance)

        purchase = Purchase(
            purchase_id=uuid.uuid4(),
            date=datetime.now(),
            party_id=party_id,
            total_taxable=total_taxable,
            total_tax=total_tax,
            grand_total=grand_total,
            paid_amount=paid_amount,
            balance_amount=balance,
            round_off=round_off,
            items=purchase_items,
        )
        for item in purchase_items:
            item.purchase_id = purchase.purchase_id

        self.purchase_repository.add_purchase(purchase)

        entries = self._build_ledger_entries(purchase.purchase_id, party, paid_amount, balance,
                                              total_taxable, total_cgst, total_sgst, total_igst)
        self.ledger_service.record_transaction(purchase.purchase_id, entries)

        return purchase

    def record_payment(self, purchase_id: UUID, amount: Decimal) -> Purchase:
        purchase = self.get_purchase(purchase_id)
        if amount > purchase.balance_amount:
            raise ValueError(f"Payment amount {amount} exceeds balance {purchase.balance_amount}")

        purchase.paid_amount += amount
        purchase.balance_amount -= amount

        if purchase.party_id:
            self.party_repository.update_balance(purchase.party_id, purchase.balance_amount)

        self.purchase_repository.update_purchase(purchase)

        party = self.party_repository.get_party(purchase.party_id) if purchase.party_id else None
        entries = [
            {'account': party_prefix(party.name) if party else "Unknown Party", 'debit': amount,
             'credit': Decimal("0"), 'desc': f"Payment made for Purchase {purchase_id}"},
            {'account': CASH, 'debit': Decimal("0"), 'credit': amount,
             'desc': f"Payment made for Purchase {purchase_id}"},
        ]
        self.ledger_service.record_transaction(uuid.uuid4(), entries)

        return purchase

    def list_purchases(self) -> list[Purchase]:
        return self.purchase_repository.list_purchases()

    def get_purchase(self, purchase_id: UUID) -> Purchase:
        purchase = self.purchase_repository.get_purchase(purchase_id)
        if not purchase:
            raise ValueError("Purchase not found")
        return purchase

    def delete_purchase(self, purchase_id: UUID) -> None:
        purchase = self.get_purchase(purchase_id)
        self._update_inventory(purchase.items, -1)
        if purchase.party_id:
            self.party_repository.update_balance(purchase.party_id, -purchase.balance_amount)
        self.ledger_service.clear_transaction(purchase.purchase_id)
        self.purchase_repository.delete_purchase(purchase_id)

    def update_purchase(self,
                        purchase_id: UUID,
                        items_data: list,
                        party_id: UUID | None = None,
                        paid_amount: Decimal = Decimal("0"),
                        round_off: bool = False,
                        tax_inclusive: bool = False) -> Purchase:
        existing = self.get_purchase(purchase_id)

        self._update_inventory(existing.items, -1)
        if existing.party_id:
            self.party_repository.update_balance(existing.party_id, -existing.balance_amount)
        self.ledger_service.clear_transaction(purchase_id)

        party, is_interstate = self._resolve_party_and_state(party_id)
        purchase_items, total_taxable, total_tax, total_cgst, total_sgst, total_igst = self._process_items(
            items_data, is_interstate, tax_inclusive)

        grand_total = compute_grand_total(total_taxable, total_tax, round_off)
        balance = max(Decimal("0"), grand_total - paid_amount)

        self._update_inventory(purchase_items, 1)
        if party_id:
            self.party_repository.update_balance(party_id, balance)

        for item in purchase_items:
            item.purchase_id = purchase_id
        self.purchase_repository.replace_items(purchase_id, purchase_items)

        existing.party_id = party_id
        existing.total_taxable = total_taxable
        existing.total_tax = total_tax
        existing.grand_total = grand_total
        existing.paid_amount = paid_amount
        existing.balance_amount = balance
        existing.round_off = round_off
        self.purchase_repository.update_purchase(existing)

        entries = self._build_ledger_entries(purchase_id, party, paid_amount, balance,
                                              total_taxable, total_cgst, total_sgst, total_igst)
        self.ledger_service.record_transaction(purchase_id, entries)

        return self.purchase_repository.get_purchase(purchase_id)
