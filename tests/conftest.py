import pytest
from sqlmodel import SQLModel, create_engine, Session

# Import models first to ensure they are registered in SQLModel.metadata
from inventory.models import Product
from parties.models import Party
from purchase.models import Purchase, PurchaseItem

@pytest.fixture(scope="session")
def engine():
    # Use in-memory SQLite for fast tests
    engine = create_engine(
        "sqlite://", 
        connect_args={"check_same_thread": False}
    )
    print(f"Registered tables: {SQLModel.metadata.tables.keys()}")
    SQLModel.metadata.create_all(engine)
    return engine

@pytest.fixture
def session(engine):
    with Session(engine) as session:
        yield session
        session.rollback()
