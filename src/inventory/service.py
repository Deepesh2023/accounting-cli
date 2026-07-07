from inventory.models import Product
from inventory.repository import Repository as InventoryRepository
import uuid

MENU_OPTIONS = {
    "1": "List products",
    "2": "Add product",
    "3": "Archive product",
    "4": "Show archived",
}


def show_menu(inventory_repository: InventoryRepository):
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

            quantity = input("Quantity: ")
            try:
                quantity = int(quantity)
            except ValueError:
                print("Error occured")
                return

            print()
            try:
                add_product(
                    name=name,
                    selling_price=selling_price,
                    quantity=quantity,
                )
            except ValueError as e:
                print(e)

        if choice == "3":
            product_id = input("Enter the product id: ")
            try:
                product = change_visibility(product_id)
                print(
                    f"{product.name}({product.product_id}) {'archived' if product.archived else 'unarchived'}."
                )

            except ValueError as e:
                print(e)

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
                f"{product.product_id}    {product.name}    {product.selling_price}    {product.quantity}"
            )


def list_products(
    inventory_repository: InventoryRepository,
    show_archived=False,
) -> list[Product]:
    products = [
        product
        for product in inventory_repository.list_products()
        if product.archived == show_archived
    ]

    return products


def add_product(
    inventory_repository: InventoryRepository,
    name: str,
    selling_price: float,
    quantity: int,
):
    if selling_price < 0 or quantity < 0:
        raise ValueError("selling-price/quantity shouldn't be negative")

    product_id = str(uuid.uuid4())

    product = Product(
        product_id=product_id,
        name=name,
        selling_price=selling_price,
        quantity=quantity,
    )
    inventory_repository.add_product(product)


def change_visibility(
    inventory_repository: InventoryRepository,
    product_id: str,
) -> Product:
    result = inventory_repository.change_visibility(product_id)
    if not result:
        raise ValueError("Product not found.")

    return result
