from inventory.models import Product
from inventory.repository import repository
import uuid

MENU_OPTIONS = {
    "1": "List products",
    "2": "Add product",
    "3": "Archive product",
    "4": "Show archived",
}


def show_menu():
    while True:
        for option, description in MENU_OPTIONS.items():
            print(f"{option}: {description}")

        choice = input("Choice: ")

        if choice == "0":
            return

        if choice not in MENU_OPTIONS.keys():
            print("Invalid option.")
            continue

        if choice == "1":
            products = list_products()
            display_products(products)

        if choice == "2":
            print("Add product")

            name = input("Name: ")

            selling_price = input("Selling price: ")
            try:
                selling_price = float(selling_price)
            except ValueError:
                print("Error occured")
                return

            qnt = input("Quantity: ")
            try:
                qnt = int(qnt)
            except ValueError:
                print("Error occured")
                return

            try:
                add_product(
                    name=name,
                    selling_price=selling_price,
                    quantity=qnt,
                )
            except ValueError as e:
                print(e)

        if choice == "3":
            id = input("Enter the product id: ")
            change_visibility(id)

        if choice == "4":
            products = list_products(show_archived=True)
            display_products(products)

        print()


def display_products(products: list[Product]):
    print()

    if len(products) == 0:
        print("No products")
    else:
        for product in products:
            print(
                f"{product.id}    {product.name}    {product.selling_price}    {product.quantity}"
            )

    print()


def list_products(show_archived=False) -> list[Product]:
    products = [
        product
        for product in repository.list_products()
        if product.archived == show_archived
    ]

    return products


def add_product(
    name: str,
    selling_price: float,
    quantity: int,
):
    if selling_price < 0 or quantity < 0:
        raise ValueError("selling-price/quantity shouldn't be negative")

    id = str(uuid.uuid4())

    product = Product(id=id, name=name, selling_price=selling_price, quantity=quantity)
    repository.add_product(product)


def change_visibility(product_id: str):
    result = repository.change_visibility(product_id)
    if not result:
        print("Product not found.")
        return

    print(f"{result.name}({result.id}) archived.")
