from fastapi import Depends
from sqlmodel import Session
from storage.database import engine

from inventory.repository import InventoryRepository
from inventory.service import InventoryService
from parties.repository import PartyRepository
from parties.service import PartyService


def get_session():
    with Session(engine) as session:
        yield session


def get_inventory_service(session: Session = Depends(get_session)) -> InventoryService:
    repo = InventoryRepository(session)
    return InventoryService(repo)


def get_parties_service(session: Session = Depends(get_session)) -> PartyService:
    repo = PartyRepository(session)
    return PartyService(repo)
