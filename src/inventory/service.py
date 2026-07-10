from inventory.models import Product
from inventory.repository import InventoryRepository
from dataclasses import replace
import uuid
from shared.exceptions import InventoryError, ProductNotFoundError, InvalidProductDataError
from shared.utils import get_input, get_confirmation

MENU_OPTIONS = {
    "1": "List products",
    "2": "Add product",
    "3": "Archive product",
    "4": "Show archived",
    "5": "edit product",
    "6": "Search product",
}


def edit_product_workflow(inventory_repository: InventoryRepository):
    product_id = input("Enter the product id: ")
    try:
        product_id = uuid.UUID(product_id)
    except ValueError:
        print("Invalid UUID format.")
        return

    product = inventory_repository.get_product(product_id=product_id)
    if not product:
        print("Product not found.")
        return

    print("The product being edited:")
    print(f"ID: {product.product_id}\nName: {product.name}\nPrice: {product.selling_price}\nQuantity: {product.quantity}")

    draft_product = replace(product)

    while True:
        field = input("Enter field to edit (name/selling_price/quantity) or 'done' to save, 'cancel' to abort: ").strip()
        
        if field == "cancel":
            print("\nEdit cancelled.")
            break
        if field == "done":
            if draft_product == product:
                print("\nNo changes made.")
                break
            
            print("\n--- Review Changes ---")
            if draft_product.name != product.name:
                print(f"Name: {product.name} -> {draft_product.name}")
            if draft_product.selling_price != product.selling_price:
                print(f"Price: {product.selling_price} -> {draft_product.selling_price}")
            if draft_product.quantity != product.quantity:
                print(f"Quantity: {product.quantity} -> {draft_product.quantity}")
            
            if get_confirmation("Confirm changes?"):
                try:
                    inventory_repository.update_product(updated_product=draft_product)
                    print("\nProduct updated successfully.")
                except ProductNotFoundError as e:
                    print(f"\nError: {e}")
            else:
                print("\nUpdate cancelled.")
            break

        if field == "name":
            new_val = get_input("Enter new name: ", str)
            draft_product.name = new_val
        elif field == "selling_price":
            draft_product.selling_price = get_input("Enter new selling price: ", float, "Invalid price. Please enter a number.")
        elif field == "quantity":
            draft_product.quantity = get_input("Enter new quantity: ", int, "Invalid quantity. Please enter an integer.")
        else:
            print("\nInvalid field. Use 'name', 'selling_price', or 'quantity'.")
    print()



def search_product_workflow(inventory_repository: InventoryRepository):
    query = input("Enter product name or ID to search: ")
    results = inventory_repository.search_products(query)
    display_products(results)


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
            products = list_products(inventory_repository=inventory_repository)
            display_products(products)

        if choice == "2":
            print("\n--- Add New Product ---")
            name = get_input("Name: ", str)
            selling_price = get_input("Selling price: ", float, "Please enter a valid number for price.")
            quantity = get_input("Quantity: ", int, "Please enter a valid integer for quantity.")

            try:
                add_product(
                    inventory_repository=inventory_repository,
                    name=name,
                    selling_price=selling_price,
                    quantity=quantity,
                )
                print("\nProduct added successfully!")
            except InvalidProductDataError as e:
                print(f"\nError: {e}")

        if choice == "3":
            product_id_str = get_input("Enter the product id to archive/unarchive: ", str)
            try:
                product_id = uuid.UUID(product_id_str)
                if get_confirmation(f"Change visibility for product {product_id_str}?"):
                    product = change_visibility(
                        inventory_repository=inventory_repository,
                        product_id=product_id,
                    )
                    status = 'unarchived' if not product.archived else 'archived'
                    print(f"\nProduct {product.name} has been {status}.")
                else:
                    print("\nOperation cancelled.")
            except ValueError:
                print("\nError: Invalid UUID format.")
            except ProductNotFoundError as e:
                print(f"\nError: {e}")

        if choice == "4":
            products = list_products(
                inventory_repository=inventory_repository,
                show_archived=True,
            )
            display_products(products)

        if choice == "5":
            edit_product_workflow(inventory_repository=inventory_repository)

        if choice == "6":
            search_product_workflow(inventory_repository=inventory_repository)




def display_products(products: list[Product]):
    print()
    if not products:
        print("No products found.")
        return

    header = f"{'ID':<38} {'Name':<20} {'Price':<10} {'Qty':<10}"
    separator = "-" * 78
    print(header)
    print(separator)

    for product in products:
        print(f"{str(product.product_id):<38} {product.name:<20} {product.selling_price:<10.2f} {product.quantity:<10}")
    print()


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
        raise InvalidProductDataError("selling-price/quantity shouldn't be negative")

    product_id = uuid.uuid4()

    product = Product(
        product_id=product_id,
        name=name,
        selling_price=selling_price,
        quantity=quantity,
    )
    inventory_repository.add_product(product)


def change_visibility(
    inventory_repository: InventoryRepository,
    product_id: uuid.UUID,
) -> Product:
    result = inventory_repository.change_visibility(product_id)
    if not result:
        raise ProductNotFoundError("Product not found.")

    return result


