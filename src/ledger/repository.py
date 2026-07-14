from uuid import UUID
from sqlmodel import Session, select, func
from ledger.models import LedgerEntry
from decimal import Decimal

class LedgerRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_entry(self, entry: LedgerEntry) -> LedgerEntry:
        self.session.add(entry)
        self.session.commit()
        self.session.refresh(entry)
        return entry

    def add_entries(self, entries: list[LedgerEntry]):
        self.session.add_all(entries)
        self.session.commit()

    def get_entries_for_account(self, account_name: str) -> list[LedgerEntry]:
        stmt = select(LedgerEntry).where(LedgerEntry.account_name == account_name)
        return self.session.execute(stmt).scalars().all()

    def get_account_balance(self, account_name: str) -> Decimal:
        """
        Calculates running balance: Total Debits - Total Credits.
        Note: For Liabilities/Equity, this value is usually interpreted as CR.
        """
        stmt = select(
            func.sum(LedgerEntry.debit), 
            func.sum(LedgerEntry.credit)
        ).where(LedgerEntry.account_name == account_name)
        
        result = self.session.execute(stmt).first()
        debit_sum = result[0] or Decimal("0")
        credit_sum = result[1] or Decimal("0")
        
        return debit_sum - credit_sum

    def delete_entries_by_transaction(self, transaction_id: UUID):
        stmt = select(LedgerEntry).where(LedgerEntry.transaction_id == transaction_id)
        entries = self.session.execute(stmt).scalars().all()
        for entry in entries:
            self.session.delete(entry)
        self.session.commit()
