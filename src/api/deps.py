from fastapi import Depends
from sqlmodel import Session
from storage.database import engine

from inventory.repository import InventoryRepository
from inventory.service import InventoryService


def get_session():
    with Session(engine) as session:
        yield session


def get_inventory_service(session: Session = Depends(get_session)) -> InventoryService:
    repo = InventoryRepository(session)
    return InventoryService(repo)
