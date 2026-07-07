from inventory.models import Product


class _Repository:
    _products: list[Product] = []

    def __init__(self):
        pass

    def add_product(self, product: Product):
        self._products.append(product)

    def list_products(self, show_archived=False):
        return [
            product for product in self._products if product.archived == show_archived
        ]

    def change_visibility(self, id: str) -> Product | None:
        for product in self._products:
            if product.id == id:
                product.archived = not product.archived
                return product

        return None


repository = _Repository()
