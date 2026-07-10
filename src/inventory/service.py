from inventory.models import Product
from inventory.repository import InventoryRepository
from dataclasses import replace
import uuid

MENU_OPTIONS = {
    "1": "List products",
    "2": "Add product",
    "3": "Archive product",
    "4": "Show archived",
    "5": "edit product",
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
            break
        if field == "done":
            if draft_product == product:
                print("No changes made.")
                break
            
            print("\nReview changes:")
            if draft_product.name != product.name:
                print(f"Name: {product.name} -> {draft_product.name}")
            if draft_product.selling_price != product.selling_price:
                print(f"Price: {product.selling_price} -> {draft_product.selling_price}")
            if draft_product.quantity != product.quantity:
                print(f"Quantity: {product.quantity} -> {draft_product.quantity}")
            
            confirm = input("Confirm changes? (y/n): ").strip().lower()
            if confirm == "y":
                try:
                    inventory_repository.update_product(updated_product=draft_product)
                    print("Product updated successfully.")
                except ValueError as e:
                    print(f"Error: {e}")
            else:
                print("Update cancelled.")
            break

        if field == "name":
            new_val = input("Enter new name: ").strip()
            if new_val:
                draft_product.name = new_val
        elif field == "selling_price":
            try:
                new_val = float(input("Enter new selling price: "))
                draft_product.selling_price = new_val
            except ValueError:
                print("Invalid price. Please enter a number.")
        elif field == "quantity":
            try:
                new_val = int(input("Enter new quantity: "))
                draft_product.quantity = new_val
            except ValueError:
                print("Invalid quantity. Please enter an integer.")
        else:
            print("Invalid field. Use 'name', 'selling_price', or 'quantity'.")
    print()

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
                    inventory_repository=inventory_repository,
                    name=name,
                    selling_price=selling_price,
                    quantity=quantity,
                )
            except ValueError as e:
                print(e)

        if choice == "3":
            product_id = input("Enter the product id: ")
            try:
                product_id = uuid.UUID(product_id)
            except ValueError:
                print("Invalid UUID format.")
                continue
            try:
                product = change_visibility(
                    inventory_repository=inventory_repository,
                    product_id=product_id,
                )
                print(
                    f"{product.name}({product.product_id}) {'archived' if product.archived else 'unarchived'}."
                )
            except ValueError as e:
                print(e)

        if choice == "4":
            products = list_products(
                inventory_repository=inventory_repository,
                show_archived=True,
            )
            display_products(products)

        if choice == "5":
            edit_product_workflow(inventory_repository=inventory_repository)




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
        raise ValueError("Product not found.")

    return result


