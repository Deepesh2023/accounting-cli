import uuid
from inventory.service import InventoryService
from shared.utils import get_input, get_confirmation, display_table
from inventory.models import Product

MENU_OPTIONS = {
    "1": "List products",
    "2": "Add product",
    "3": "Archive product",
    "4": "Show archived",
    "5": "edit product",
    "6": "Search product",
}

def show_menu(service: InventoryService):
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
            products = service.list_products(show_archived=False)
            display_products(products)

        if choice == "2":
            print("\n--- Add New Product ---")
            name = get_input("Name: ", str)
            selling_price = get_input("Selling price: ", float, "Please enter a valid number for price.")
            quantity = get_input("Quantity: ", int, "Please enter a valid integer for quantity.")

            try:
                service.add_product(name=name, selling_price=selling_price, quantity=quantity)
                print("\nProduct added successfully!")
            except Exception as e:
                print(f"\nError: {e}")

        if choice == "3":
            product_id_str = get_input("Enter the product id to archive/unarchive: ", str)
            try:
                product_id = uuid.UUID(product_id_str)
                if get_confirmation(f"Change visibility for product {product_id_str}?"):
                    product = service.change_visibility(product_id=product_id)
                    status = 'unarchived' if not product.archived else 'archived'
                    print(f"\nProduct {product.name} has been {status}.")
                else:
                    print("\nOperation cancelled.")
            except ValueError:
                print("\nError: Invalid UUID format.")
            except Exception as e:
                print(f"\nError: {e}")

        if choice == "4":
            products = service.list_products(show_archived=True)
            display_products(products)

        if choice == "5":
            edit_product_workflow(service)

        if choice == "6":
            search_product_workflow(service)

def search_product_workflow(service: InventoryService):
    query = input("Enter product name or ID to search: ")
    results = service.search_products(query)
    display_products(results)

def edit_product_workflow(service: InventoryService):
    product_id = input("Enter the product id: ")
    try:
        product_id = uuid.UUID(product_id)
    except ValueError:
        print("Invalid UUID format.")
        return

    try:
        product = service.get_product(product_id)
    except Exception:
        print("Product not found.")
        return

    print("The product being edited:")
    print(f"ID: {product.product_id}\nName: {product.name}\nPrice: {product.selling_price}\nQuantity: {product.quantity}")

    from dataclasses import replace
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
                    service.update_product(draft_product)
                    print("\nProduct updated successfully.")
                except Exception as e:
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

def display_products(products: list[Product]):
    header = f"{'ID':<38} {'Name':<20} {'Price':<10} {'Qty':<10}"
    rows = [
        f"{str(product.product_id):<38} {product.name:<20} {product.selling_price:<10.2f} {product.quantity:<10}"
        for product in products
    ]
    display_table(header, rows)
