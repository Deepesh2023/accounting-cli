import uuid
from uuid import UUID
from decimal import Decimal
from ledger.models import LedgerEntry
from ledger.repository import LedgerRepository

class LedgerService:
    def __init__(self, repository: LedgerRepository):
        self.repository = repository

    def record_transaction(self, transaction_id: UUID, entries: list[dict]):
        """
        Expects a list of entries: [{'account': str, 'debit': Decimal, 'credit': Decimal, 'desc': str}]
        """
        total_debit = sum(e['debit'] for e in entries)
        total_credit = sum(e['credit'] for e in entries)

        if total_debit != total_credit:
            raise ValueError(f"Transaction unbalanced: DR {total_debit} != CR {total_credit}")

        ledger_entries = [
            LedgerEntry(
                entry_id=uuid.uuid4(),
                account_name=e['account'],
                debit=e['debit'],
                credit=e['credit'],
                transaction_id=transaction_id,
                description=e.get('desc', '')
            )
            for e in entries
        ]
        
        self.repository.add_entries(ledger_entries)

    def get_balance(self, account_name: str) -> Decimal:
        return self.repository.get_account_balance(account_name)

    def get_entries_for_account(self, account_name: str) -> list[LedgerEntry]:
        return self.repository.get_entries_for_account(account_name)

    def get_gst_summary(self) -> dict:
        """Returns the balance of all GST related accounts."""
        gst_accounts = ['Input CGST', 'Input SGST', 'Input IGST', 'Output CGST', 'Output SGST', 'Output IGST']
        summary = {}
        for acc in gst_accounts:
            summary[acc] = self.get_balance(acc)
        return summary

    def get_account_balances(self, accounts: list[str]) -> dict[str, Decimal]:
        """Returns balances for a set of accounts, e.g., ['Cash', 'Bank']."""
        return {acc: self.get_balance(acc) for acc in accounts}

    def list_all_transactions(self) -> list[LedgerEntry]:

        return self.repository.list_all_entries()

    def clear_transaction(self, transaction_id: UUID):
        self.repository.delete_entries_by_transaction(transaction_id)
