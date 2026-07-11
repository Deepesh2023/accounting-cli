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
        pass

    def add_sale(self, sale: Sale):
        self._sales.append(sale)
        self._save_to_disk()

    def list_sales(self) -> list[Sale]:
        return self._sales.copy()
