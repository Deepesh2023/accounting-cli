from datetime import date
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

from main import app
from api.deps import get_session

import inventory.models  # noqa: F401
import quotation.models  # noqa: F401
import sale.models  # noqa: F401
import parties.models  # noqa: F401
import expenses.models  # noqa: F401
import purchase.models  # noqa: F401
import ledger.models  # noqa: F401
import company.models  # noqa: F401

_TEST_ENGINE = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SQLModel.metadata.create_all(_TEST_ENGINE)


def get_test_session():
    with Session(_TEST_ENGINE) as session:
        yield session


def _clean_db():
    with _TEST_ENGINE.connect() as conn:
        for table in reversed(SQLModel.metadata.sorted_tables):
            conn.execute(table.delete())
        conn.commit()


def client():
    _clean_db()
    app.dependency_overrides[get_session] = get_test_session
    yield TestClient(app)
    app.dependency_overrides.clear()


class TestGetProfile:
    def test_not_found(self):
        gen = client()
        c = next(gen)
        resp = c.get("/api/company")
        assert resp.status_code == 404


    def test_found(self):
        gen = client()
        c = next(gen)
        c.put("/api/company", json={"name": "Nectar Technologies"})
        resp = c.get("/api/company")
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "Nectar Technologies"


class TestUpsertProfile:
    def test_creates(self):
        gen = client()
        c = next(gen)
        resp = c.put("/api/company", json={
            "name": "Nectar Technologies",
            "business_type": "Retail",
            "phone": "+91 9876543210",
            "email": "contact@nectar.com",
            "address": "123 Tech Park, Bangalore",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "Nectar Technologies"
        assert data["business_type"] == "Retail"
        assert data["phone"] == "+91 9876543210"
        assert data["email"] == "contact@nectar.com"
        assert data["address"] == "123 Tech Park, Bangalore"

    def test_updates_existing(self):
        gen = client()
        c = next(gen)
        c.put("/api/company", json={"name": "Nectar Technologies"})
        resp = c.put("/api/company", json={
            "name": "Nectar Tech Solutions",
            "business_type": "IT Services",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "Nectar Tech Solutions"
        assert data["business_type"] == "IT Services"

    def test_with_dates(self):
        gen = client()
        c = next(gen)
        resp = c.put("/api/company", json={
            "name": "Test Corp",
            "beginning_date": "2023-01-01",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["beginning_date"] == "2023-01-01"
