import pytest
from sqlmodel import SQLModel, create_engine, Session

@pytest.fixture(scope="session")
def engine():
    # Use in-memory SQLite for fast tests
    # check_same_thread=False is required for SQLite when using multi-threading
    engine = create_engine(
        "sqlite://", 
        connect_args={"check_same_thread": False}
    )
    SQLModel.metadata.create_all(engine)
    return engine

@pytest.fixture
def session(engine):
    with Session(engine) as session:
        yield session
        session.rollback() # Clean up after each test
