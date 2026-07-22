class TestGetProfile:
    def test_not_found(self, client):
        resp = client.get("/api/company")
        assert resp.status_code == 404

    def test_found(self, client):
        client.put("/api/company", json={"name": "Nectar Technologies"})
        resp = client.get("/api/company")
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "Nectar Technologies"


class TestUpsertProfile:
    def test_creates(self, client):
        resp = client.put("/api/company", json={
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

    def test_updates_existing(self, client):
        client.put("/api/company", json={"name": "Nectar Technologies"})
        resp = client.put("/api/company", json={
            "name": "Nectar Tech Solutions",
            "business_type": "IT Services",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "Nectar Tech Solutions"
        assert data["business_type"] == "IT Services"

    def test_with_dates(self, client):
        resp = client.put("/api/company", json={
            "name": "Test Corp",
            "beginning_date": "2023-01-01",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["beginning_date"] == "2023-01-01"
