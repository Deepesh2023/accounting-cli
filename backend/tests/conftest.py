import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, create_engine, Session

# Import all models to register them on SQLModel.metadata
import inventory.models  # noqa: F401
import parties.models  # noqa: F401
import purchase.models  # noqa: F401
import quotation.models  # noqa: F401
import sale.models  # noqa: F401
import expenses.models  # noqa: F401
import ledger.models  # noqa: F401
import company.models  # noqa: F401

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
    from main import app
    from api.deps import get_session

    app.dependency_overrides[get_session] = get_test_session
    yield TestClient(app)
    app.dependency_overrides.clear()
