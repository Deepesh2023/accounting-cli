from models import Product


class Inventory:
    _products: list[Product] = []

    def __init__(self):
        pass

    def add_product(self, product: Product):
        self._products.append(product)
