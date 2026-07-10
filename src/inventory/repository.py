from inventory.models import Product
import uuid


class Repository:
    def __init__(self):
        self._products: list[Product] = []

    def add_product(self, product: Product):
        self._products.append(product)

    def get_product(self, product_id: uuid) -> Product | None:
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
                return product

        return None

    def update_product(self, updated_product: Product):
        product = self.get_product(product_id=updated_product.product_id)
        if not product:
            raise ValueError("Cannot find product.")

        product.name = updated_product.name
        product.selling_price = updated_product.selling_price
        product.quantity = updated_product.quantity
