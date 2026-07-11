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
