from inventory.models import Product
import uuid
import json
import os
from uuid import UUID
from shared.exceptions import ProductNotFoundError


class InventoryRepository:
    def __init__(self, storage_file="inventory.json"):
        self._storage_file = storage_file
        self._products: list[Product] = self._load_from_disk()

    def _load_from_disk(self) -> list[Product]:
        if not os.path.exists(self._storage_file):
            return []
        
        try:
            with open(self._storage_file, "r") as f:
                data = json.load(f)
                return [
                    Product(
                        product_id=UUID(item["product_id"]),
                        name=item["name"],
                        selling_price=item["selling_price"],
                        quantity=item["quantity"],
                        archived=item["archived"]
                    )
                    for item in data
                ]
        except (json.JSONDecodeError, KeyError, ValueError):
            return []

    def _save_to_disk(self):
        data = [
            {
                "product_id": str(p.product_id),
                "name": p.name,
                "selling_price": p.selling_price,
                "quantity": p.quantity,
                "archived": p.archived
            }
            for p in self._products
        ]
        with open(self._storage_file, "w") as f:
            json.dump(data, f, indent=4)

    def add_product(self, product: Product):
        self._products.append(product)
        self._save_to_disk()

    def get_product(self, product_id: UUID) -> Product | None:
        for product in self._products:
            if product.product_id == product_id:
                return product

        return None

    def list_products(self) -> list[Product]:
        return self._products.copy()

    def change_visibility(self, product_id: uuid.UUID) -> Product | None:
        for product in self._products:
            if product.product_id == product_id:
                product.archived = not product.archived
                self._save_to_disk()
                return product

        return None

    def update_product(self, updated_product: Product):
        product = self.get_product(product_id=updated_product.product_id)
        if not product:
            raise ProductNotFoundError("Cannot find product.")

        product.name = updated_product.name
        product.selling_price = updated_product.selling_price
        product.quantity = updated_product.quantity
        self._save_to_disk()
