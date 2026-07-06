from inventory.models import Product


class _Inventory:
    _products: list[Product] = []

    def __init__(self):
        pass

    def add_product(self, product: Product):
        self._products.append(product)

    def list_products(self, show_archived=False):
        if show_archived:
            return self._products

        return [product for product in self._products if not product.archived]

    def change_visibilty(self, id: str) -> Product | None:
        for product in self._products:
            if product.id == id:
                product.archived = not product.archived
                return product

        return None


inventory = _Inventory()
