from fastapi import Depends
from sqlmodel import Session
from src.storage.database import engine
from src.inventory.repository import InventoryRepository
from src.inventory.service import InventoryService
from src.parties.repository import PartyRepository
from src.parties.service import PartyService
from src.sale.repository import SaleRepository
from src.sale.service import SaleService
from src.purchase.repository import PurchaseRepository
from src.purchase.service import PurchaseService
from src.expenses.repository import ExpenseRepository
from src.expenses.service import ExpenseService
from src.quotation.repository import QuotationRepository
from src.quotation.service import QuotationService
from src.reports.service import ReportService
from src.company.repository import CompanyRepository
from src.company.service import CompanyService
from src.ledger.repository import LedgerRepository
from src.ledger.service import LedgerService


def get_session():
    with Session(engine) as session:
        yield session


def get_inventory_service(session: Session = Depends(get_session)) -> InventoryService:
    repo = InventoryRepository(session)
    return InventoryService(repo)


def get_parties_service(session: Session = Depends(get_session)) -> PartyService:
    repo = PartyRepository(session)
    return PartyService(repo)


def get_sale_service(session: Session = Depends(get_session)) -> SaleService:
    sale_repo = SaleRepository(session)
    inv_repo = InventoryRepository(session)
    party_repo = PartyRepository(session)
    ledger_svc = LedgerService(LedgerRepository(session))
    return SaleService(sale_repo, inv_repo, party_repo, ledger_svc)


def get_purchase_service(session: Session = Depends(get_session)) -> PurchaseService:
    purchase_repo = PurchaseRepository(session)
    inv_repo = InventoryRepository(session)
    party_repo = PartyRepository(session)
    ledger_svc = LedgerService(LedgerRepository(session))
    return PurchaseService(purchase_repo, inv_repo, party_repo, ledger_svc)


def get_expense_service(session: Session = Depends(get_session)) -> ExpenseService:
    repo = ExpenseRepository(session)
    ledger_svc = LedgerService(LedgerRepository(session))
    return ExpenseService(repo, ledger_service=ledger_svc)


def get_quotation_service(session: Session = Depends(get_session)) -> QuotationService:
    repo = QuotationRepository(session)
    return QuotationService(repo)


def get_company_service(session: Session = Depends(get_session)) -> CompanyService:
    repo = CompanyRepository(session)
    return CompanyService(repo)


def get_ledger_service(session: Session = Depends(get_session)) -> LedgerService:
    repo = LedgerRepository(session)
    return LedgerService(repo)


def get_report_service(session: Session = Depends(get_session)) -> ReportService:
    inv_repo = InventoryRepository(session)
    party_repo = PartyRepository(session)
    ledger_svc = LedgerService(LedgerRepository(session))
    return ReportService(inv_repo, party_repo, ledger_svc)
