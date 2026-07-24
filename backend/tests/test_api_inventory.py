import pytest
from uuid import uuid4
from decimal import Decimal

from src.inventory.repository import InventoryRepository
from src.inventory.service import InventoryService


@pytest.fixture
def service(session):
    return InventoryService(InventoryRepository(session))


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
        p2 = service.add_product("Visible", Decimal("20"), 3)
        service.change_visibility(p1.product_id)

        resp = client.get("/api/inventory?show_archived=true")
        data = resp.json()
        assert len(data) == 2
        names = {d["name"] for d in data}
        assert names == {"Active", "Visible"}

        resp = client.get("/api/inventory?show_archived=false")
        data = resp.json()
        assert len(data) == 1
        assert data[0]["name"] == "Visible"


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
