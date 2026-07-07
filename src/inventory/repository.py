from inventory.models import Product


class Repository:
    def __init__(self):
        self._products: list[Product] = []

    def add_product(self, product: Product):
        self._products.append(product)

    def list_products(self) -> list[Product]:
        return self._products.copy()

    def change_visibility(self, product_id: str) -> Product | None:
        for product in self._products:
            if product.product_id == product_id:
                product.archived = not product.archived
                return product

        return None
