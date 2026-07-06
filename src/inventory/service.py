from inventory.models import Product
from inventory.repository import inventory
import uuid

MENU_OPTIONS = {
    "1": "List products",
    "2": "Add product",
    "3": "Archive product",
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


    print("=" * 28 + "\n")

        print("No products.")
        return


    print("=" * 28 + "\n")


def change_visibility(id: str):
    result = inventory.change_visibility(id)
    if not result:
        print("Product not found.")
        return

    print(f"{result.name}({result.id}) archived.")
