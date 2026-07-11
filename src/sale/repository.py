import json
import os
from uuid import UUID
from datetime import datetime
from sale.models import Sale, SaleItem

class SaleRepository:
    def __init__(self, storage_file="sales.json"):
        self._storage_file = storage_file
        self._sales: list[Sale] = self._load_from_disk()

    def _load_from_disk(self) -> list[Sale]:
        if not os.path.exists(self._storage_file):
            return []
        
        try:
            with open(self._storage_file, "r") as f:
                data = json.load(f)
                return [
                    Sale(
                        sale_id=UUID(item["sale_id"]),
                        date=datetime.fromisoformat(item["date"]),
                        items=[
                            SaleItem(
                                product_id=UUID(si["product_id"]),
                                name=si["name"],
                                selling_price=si["selling_price"],
                                quantity=si["quantity"]
                            )
                            for si in item["items"]
                        ],
                        customer_name=item.get("customer_name")
                    )
                    for item in data
                ]
        except (json.JSONDecodeError, KeyError, ValueError):
            return []

    def _save_to_disk(self):
        data = [
            {
                "sale_id": str(s.sale_id),
                "date": s.date.isoformat(),
                "customer_name": s.customer_name,
                "items": [
                    {
                        "product_id": str(si.product_id),
                        "name": si.name,
                        "selling_price": si.selling_price,
                        "quantity": si.quantity
                    }
                    for si in s.items
                ]
            }
            for s in self._sales
        ]
        with open(self._storage_file, "w") as f:
            json.dump(data, f, indent=4)

    def add_sale(self, sale: Sale):
        self._sales.append(sale)
        self._save_to_disk()

    def list_sales(self) -> list[Sale]:
        return self._sales.copy()

    def get_sale(self, sale_id: UUID) -> Sale | None:
        for sale in self._sales:
            if sale.sale_id == sale_id:
                return sale
        return None
