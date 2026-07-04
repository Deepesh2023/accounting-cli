from inventory.models import Product
import uuid

MENU_OPTIONS = {
    "1": "Add product",
    "2": "Remove product",
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

            add_product(name=name, selling_price=selling_price, quantity=qnt)


def add_product(name: str, selling_price: float, quantity: int):
    if selling_price < 0 or quantity < 0:
        print("Error")
        return

    id = str(uuid.uuid4())

    product = Product(id=id, name=name, selling_price=selling_price, quantity=quantity)
    print(product)
