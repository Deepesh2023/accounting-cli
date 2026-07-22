import pytest
from uuid import uuid4
from decimal import Decimal
from fastapi.testclient import TestClient
from sqlalchemy import inspect
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool

from main import app
from api.deps import get_inventory_service, get_session
from inventory.repository import InventoryRepository
from inventory.service import InventoryService

import inventory.models  # noqa: F401  register tables on SQLModel.metadata
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


@pytest.fixture(autouse=True)
def _clean_db():
    with _TEST_ENGINE.connect() as conn:
        for table in reversed(SQLModel.metadata.sorted_tables):
            conn.execute(table.delete())
        conn.commit()


@pytest.fixture
def service():
    return InventoryService(InventoryRepository(Session(_TEST_ENGINE)))


@pytest.fixture
def client():
    app.dependency_overrides[get_session] = get_test_session
    yield TestClient(app)
    app.dependency_overrides.clear()


class TestListProducts:
    def test_empty(self, client):
        resp = client.get("/api/inventory")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_returns_products(self, client, service):
        service.add_product("Apple", Decimal("10"), 5)
        service.add_product("Banana", Decimal("20"), 10)

        resp = client.get("/api/inventory")
        data = resp.json()
        assert len(data) == 2
        assert data[0]["name"] == "Apple"
        assert data[1]["name"] == "Banana"

    def test_filters_archived(self, client, service):
        p1 = service.add_product("Active", Decimal("10"), 5)
        service.change_visibility(p1.product_id)

        resp = client.get("/api/inventory?show_archived=true")
        data = resp.json()
        assert len(data) == 1
        assert data[0]["name"] == "Active"

        resp = client.get("/api/inventory?show_archived=false")
        assert len(resp.json()) == 0


class TestGetProduct:
    def test_not_found(self, client):
        resp = client.get(f"/api/inventory/{uuid4()}")
        assert resp.status_code == 404

    def test_found(self, client, service):
        p = service.add_product("Laptop", Decimal("50000"), 3)
        resp = client.get(f"/api/inventory/{p.product_id}")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Laptop"
        assert Decimal(resp.json()["selling_price"]) == Decimal("50000")


class TestCreateProduct:
    def test_creates(self, client):
        resp = client.post("/api/inventory", json={
            "name": "Widget",
            "selling_price": "100.00",
            "quantity": 10,
            "gst_rate": "18",
            "hsn_code": "1234",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Widget"
        assert Decimal(data["selling_price"]) == Decimal("100.00")
        assert data["quantity"] == 10

    def test_invalid_data(self, client):
        resp = client.post("/api/inventory", json={
            "name": "Bad",
            "selling_price": "-10",
            "quantity": 5,
        })
        assert resp.status_code == 400


class TestUpdateProduct:
    def test_updates(self, client, service):
        p = service.add_product("Old", Decimal("50"), 2)
        resp = client.put(f"/api/inventory/{p.product_id}", json={
            "name": "New",
            "selling_price": "75",
            "quantity": 10,
        })
        assert resp.status_code == 200
        assert resp.json()["name"] == "New"
        assert Decimal(resp.json()["selling_price"]) == Decimal("75")

    def test_not_found(self, client):
        resp = client.put(f"/api/inventory/{uuid4()}", json={
            "name": "X",
            "selling_price": "10",
            "quantity": 1,
        })
        assert resp.status_code == 404


class TestDeleteProduct:
    def test_deletes(self, client, service):
        p = service.add_product("Delete Me", Decimal("10"), 1)
        resp = client.delete(f"/api/inventory/{p.product_id}")
        assert resp.status_code == 204

        resp = client.get(f"/api/inventory/{p.product_id}")
        assert resp.status_code == 404

    def test_not_found(self, client):
        resp = client.delete(f"/api/inventory/{uuid4()}")
        assert resp.status_code == 404
