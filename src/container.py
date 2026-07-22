from sqlalchemy.orm import Session
from storage.database import get_db

from inventory.repository import InventoryRepository
from inventory.service import InventoryService
from sale.repository import SaleRepository
from sale.service import SaleService
from purchase.repository import PurchaseRepository
from purchase.service import PurchaseService
from parties.repository import PartyRepository
from parties.service import PartyService
from expenses.repository import ExpenseRepository
from expenses.service import ExpenseService
from ledger.repository import LedgerRepository
from ledger.service import LedgerService
from quotation.repository import QuotationRepository
from quotation.service import QuotationService
from company.repository import CompanyRepository
from company.service import CompanyService
from reports.service import ReportService


class Container:
    def __init__(self):
        self.session: Session = next(get_db())

        # Repositories
        self.inventory_repository = InventoryRepository(self.session)
        self.sale_repository = SaleRepository(self.session)
        self.purchase_repository = PurchaseRepository(self.session)
        self.party_repository = PartyRepository(self.session)
        self.expense_repository = ExpenseRepository(self.session)
        self.ledger_repository = LedgerRepository(self.session)
        self.quotation_repository = QuotationRepository(self.session)
        self.company_repository = CompanyRepository(self.session)

        # Services
        self.ledger_service = LedgerService(self.ledger_repository)
        self.inventory_service = InventoryService(self.inventory_repository)
        self.party_service = PartyService(self.party_repository)
        self.sale_service = SaleService(
            self.sale_repository,
            self.inventory_repository,
            self.party_repository,
            self.ledger_service,
        )
        self.purchase_service = PurchaseService(
            self.purchase_repository,
            self.inventory_repository,
            self.party_repository,
            self.ledger_service,
        )
        self.expense_service = ExpenseService(
            self.expense_repository,
            ledger_service=self.ledger_service,
        )
        self.quotation_service = QuotationService(self.quotation_repository)
        self.company_service = CompanyService(self.company_repository)
        self.report_service = ReportService(
            self.inventory_repository,
            self.party_repository,
            self.ledger_service,
        )


container = Container()
