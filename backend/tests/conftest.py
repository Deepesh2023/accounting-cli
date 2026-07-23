import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, create_engine, Session

# Import all models to register them on SQLModel.metadata
import src.inventory.models  # noqa: F401
import src.parties.models  # noqa: F401
import src.purchase.models  # noqa: F401
import src.quotation.models  # noqa: F401
import src.sale.models  # noqa: F401
import src.expenses.models  # noqa: F401
import src.ledger.models  # noqa: F401
import src.company.models  # noqa: F401

_TEST_ENGINE = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SQLModel.metadata.create_all(_TEST_ENGINE)


@pytest.fixture(autouse=True)
def _clean_db():
    with _TEST_ENGINE.connect() as conn:
        for table in reversed(SQLModel.metadata.sorted_tables):
            conn.execute(table.delete())
        conn.commit()


def get_test_session():
    with Session(_TEST_ENGINE) as session:
        yield session


@pytest.fixture
def session():
    with Session(_TEST_ENGINE) as session:
        yield session


@pytest.fixture
def client():
    from src.main import app
    from src.api.deps import get_session

    app.dependency_overrides[get_session] = get_test_session
    yield TestClient(app)
    app.dependency_overrides.clear()
