from fastapi import Depends
from sqlmodel import Session
from storage.database import engine

from inventory.repository import InventoryRepository
from inventory.service import InventoryService
from parties.repository import PartyRepository
from parties.service import PartyService
from sale.repository import SaleRepository
from sale.service import SaleService
from ledger.service import LedgerService
from ledger.repository import LedgerRepository


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
