from decimal import Decimal
from typing import Dict
from inventory.repository import InventoryRepository
from parties.repository import PartyRepository
from ledger.service import LedgerService

class ReportService:
    def __init__(self, 
                 inventory_repository: InventoryRepository, 
                 party_repository: PartyRepository, 
                 ledger_service: LedgerService):
        self.inventory_repository = inventory_repository
        self.party_repository = party_repository
        self.ledger_service = ledger_service

    def get_trading_account(self) -> Dict:
        """
        Gross Profit = (Sales + Closing Stock) - Purchases
        """
        sales = abs(self.ledger_service.get_balance("Sales Revenue"))
        purchases = abs(self.ledger_service.get_balance("Purchases"))
        
        # Closing Stock = Sum of (Qty * Price) for all items
        products = self.inventory_repository.list_products()
        closing_stock = sum((p.quantity * p.selling_price for p in products), Decimal("0"))
        
        gross_profit = (sales + closing_stock) - purchases
        
        return {
            "sales": sales,
            "closing_stock": closing_stock,
            "purchases": purchases,
            "gross_profit": gross_profit,
            "is_loss": gross_profit < 0
        }

    def get_profit_and_loss(self, gross_profit: Decimal) -> Dict:
        """
        Net Profit = (Gross Profit + Incomes) - Expenses
        """
        incomes = abs(self.ledger_service.get_balance("Other Income"))
        expenses = abs(self.ledger_service.get_balance("Expenses"))
        
        net_profit = (gross_profit + incomes) - expenses
        
        return {
            "gross_profit": gross_profit,
            "incomes": incomes,
            "expenses": expenses,
            "net_profit": net_profit,
            "is_loss": net_profit < 0
        }

    def get_outstanding_report(self) -> list[dict]:
        """
        Returns a list of parties with non-zero balances, 
        identifying them as Debtors (positive) or Creditors (negative).
        """
        parties = self.party_repository.list_parties()
        report = []
        
        for party in parties:
            if party.balance != 0:
                report.append({
                    "party_id": party.party_id,
                    "name": party.name,
                    "balance": party.balance,
                    "type": "Debtor" if party.balance > 0 else "Creditor",
                    "amount_due": abs(party.balance)
                })
        
        return report

    def get_transaction_history(self) -> list[dict]:
        """
        Returns all ledger transactions sorted by date.
        """
        try:
            transactions = self.ledger_service.list_all_transactions()
            return transactions
        except AttributeError:
            return []

    def get_balance_sheet(self) -> Dict:
        """
        Assets = Liabilities + Equity
        """
        # 1. Assets
        cash_balance = self.ledger_service.get_balance("Cash")
        products = self.inventory_repository.list_products()
        closing_stock = sum((p.quantity * p.selling_price for p in products), Decimal("0"))
        
        # Gross Debtors: Sum of positive balances in Party domain
        parties = self.party_repository.list_parties()
        gross_debtors = sum((p.balance for p in parties if p.balance > 0), Decimal("0"))
        
        total_assets = cash_balance + closing_stock + gross_debtors
        
        # 2. Liabilities & Equity
        # Gross Creditors: Sum of negative balances (absolute)
        gross_creditors = sum((abs(p.balance) for p in parties if p.balance < 0), Decimal("0"))
        
        # Capital/Equity usually starts from a specific account
        capital = abs(self.ledger_service.get_balance("Capital"))
        
        # Net Profit from P&L
        trading = self.get_trading_account()
        pl = self.get_profit_and_loss(trading["gross_profit"])
        net_profit = pl["net_profit"]
        
        total_liabilities_equity = gross_creditors + capital + net_profit
        
        return {
            "assets": {
                "cash": cash_balance,
                "closing_stock": closing_stock,
                "debtors": gross_debtors,
                "total": total_assets
            },
            "liabilities_equity": {
                "creditors": gross_creditors,
                "capital": capital,
                "net_profit": net_profit,
                "total": total_liabilities_equity
            },
            "is_balanced": total_assets == total_liabilities_equity
        }
