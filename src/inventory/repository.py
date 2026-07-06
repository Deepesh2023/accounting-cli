from models import Product


class _Inventory:
    _products: list[Product] = []

    def __init__(self):
        pass

    def add_product(self, product: Product):
        self._products.append(product)
