from inventory.models import Product
from inventory.repository import inventory
import uuid

MENU_OPTIONS = {
    "1": "List products",
    "2": "Add product",
    "3": "Remove product",
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
            list_products()

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

            add_product(
                name=name,
                selling_price=selling_price,
                quantity=qnt,
            )

        print()


def add_product(
    name: str,
    selling_price: float,
    quantity: int,
):
    if selling_price < 0 or quantity < 0:
        print("Error")
        return

    id = str(uuid.uuid4())

    product = Product(id=id, name=name, selling_price=selling_price, quantity=quantity)
    inventory.add_product(product)

    print("Product added.")


def list_products():
    print("=" * 28 + "\n")

    if len(inventory.list_products()) == 0:
        print("No products.")
        return

    print("Name    price   quantity")
    for product in inventory.list_products():
        print(f"{product.name}    {product.selling_price}    {product.quantity}")

    print("=" * 28 + "\n")
