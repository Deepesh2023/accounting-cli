import uuid
from datetime import datetime
from typing import List, Optional
from dataclasses import replace

from sale.models import Sale, SaleItem
from sale.repository import SaleRepository
from inventory.repository import InventoryRepository
from shared.utils import get_input, get_confirmation
from inventory.service import search_product_workflow

SALE_MENU_OPTIONS = {
    "1": "Record a sale",
    "2": "View sale history",
}


def show_menu(
    inventory_repository: InventoryRepository, sale_repository: SaleRepository
):
    while True:
        for option, description in SALE_MENU_OPTIONS.items():
            print(f"{option}: {description}")

        choice = input("Choice: ")

        if choice == "0":
            return

        if choice not in SALE_MENU_OPTIONS.keys():
            print("Invalid option.")
            continue

        if choice == "1":
            record_sale_workflow(inventory_repository, sale_repository)

        if choice == "2":
            view_sales_history(sale_repository)


def record_sale_workflow(
    inventory_repository: InventoryRepository, sale_repository: SaleRepository
):
    selling_items: List[SaleItem] = []

    while True:
        print("\n--- Record Sale ---")
        print("Current Selling List:")
        display_selling_items(selling_items)

        print("\nOptions:")
        print("1: Add item from inventory")
        print("2: Remove item")
        print("3: Edit item")
        print("4: Confirm sale")
        print("S: Search for product ID")
        print("0: Cancel and return")

        choice = input("Choice: ")

        if choice == "0":
            print("Sale cancelled.")
            return

        if choice == "5":
            search_product_workflow(inventory_repository)
            continue

        if choice == "1":
            item = add_item_to_list(inventory_repository)
            if item:
                # Merge if same product and same price
                existing = next(
                    (
                        si
                        for si in selling_items
                        if si.product_id == item.product_id
                        and si.selling_price == item.selling_price
                    ),
                    None,
                )
                if existing:
                    existing.quantity += item.quantity
                else:
                    selling_items.append(item)

        elif choice == "2":
            remove_item_from_list(selling_items)

        elif choice == "3":
            edit_item_in_list(selling_items, inventory_repository)

        elif choice == "4":
            if not selling_items:
                print("Sale must contain at least one item.")
                continue

            if get_confirmation("Confirm this sale?"):
                confirm_sale(inventory_repository, sale_repository, selling_items)
                print("\nSale recorded successfully!")
                return
            else:
                print("\nConfirmation cancelled.")
        else:
            print("Invalid option.")


def add_item_to_list(inventory_repository: InventoryRepository) -> Optional[SaleItem]:
    product_id_str = get_input("Enter Product ID: ", str)
    try:
        product_id = uuid.UUID(product_id_str)
    except ValueError:
        print("Invalid UUID format.")
        return None

    product = inventory_repository.get_product(product_id)
    if not product or product.archived:
        print("Product not found or archived.")
        return None

    print(
        f"Selected: {product.name} | Price: {product.selling_price} | Stock: {product.quantity}"
    )

    price = (
        get_input(f"Selling Price [{product.selling_price}]: ", float)
        or product.selling_price
    )
    quantity = get_input(f"Quantity [{product.quantity}]: ", int) or 1

    if price < 0:
        print("Warning: Selling price cannot be negative.")
        return None
    if quantity <= 0:
        print("Warning: Quantity must be greater than zero.")
        return None
    if quantity > product.quantity:
        print(f"Warning: Quantity exceeds available stock ({product.quantity}).")
        return None

    return SaleItem(
        product_id=product.product_id,
        name=product.name,
        selling_price=price,
        quantity=quantity,
    )


def remove_item_from_list(selling_items: List[SaleItem]):
    if not selling_items:
        print("List is empty.")
        return

    for i, item in enumerate(selling_items):
        print(f"{i}: {item.name} x {item.quantity}")

    idx_str = get_input("Enter index to remove: ", int)
    if 0 <= idx_str < len(selling_items):
        selling_items.pop(idx_str)
    else:
        print("Invalid index.")


def edit_item_in_list(
    selling_items: List[SaleItem], inventory_repository: InventoryRepository
):
    if not selling_items:
        print("List is empty.")
        return

    for i, item in enumerate(selling_items):
        print(f"{i}: {item.name} x {item.quantity} @ {item.selling_price}")

    idx_str = get_input("Enter index to edit: ", int)
    if not (0 <= idx_str < len(selling_items)):
        print("Invalid index.")
        return

    item = selling_items[idx_str]
    product = inventory_repository.get_product(item.product_id)

    price = (
        get_input(f"New Price [{item.selling_price}]: ", float) or item.selling_price
    )
    quantity = get_input(f"New Quantity [{item.quantity}]: ", int) or item.quantity

    if price < 0:
        print("Error: Price cannot be negative.")
        return
    if quantity <= 0:
        print("Error: Quantity must be greater than zero.")
        return
    if product and quantity > product.quantity:
        print(f"Error: Quantity exceeds stock ({product.quantity}).")
        return

    item.selling_price = price
    item.quantity = quantity


def confirm_sale(
    inventory_repository: InventoryRepository,
    sale_repository: SaleRepository,
    items: List[SaleItem],
):
    # 1. Update Inventory
    for item in items:
        product = inventory_repository.get_product(item.product_id)
        if product:
            product.quantity -= item.quantity
            inventory_repository.update_product(product)

    # 2. Record Sale
    sale = Sale(
        sale_id=uuid.uuid4(),
        date=datetime.now(),
        items=items,
        customer_name=None,  # Simplified for now
    )
    sale_repository.add_sale(sale)


def view_sales_history(sale_repository: SaleRepository):
    sales = sale_repository.list_sales()
    if not sales:
        print("\nNo sales recorded yet.")
        return

    print("\n--- Sale History ---")
    for sale in sales:
        print(f"ID: {sale.sale_id} | Date: {sale.date} | Items: {len(sale.items)}")
        for item in sale.items:
            print(f"  - {item.name} x {item.quantity} @ {item.selling_price}")
        print("-" * 20)


def display_selling_items(items: List[SaleItem]):
    if not items:
        print("No items in list.")
        return

    header = f"{'Item':<20} {'Price':<10} {'Qty':<10} {'Subtotal':<10}"
    print(header)
    print("-" * 50)

    total = 0
    total_qty = 0
    for item in items:
        subtotal = item.selling_price * item.quantity
        total += subtotal
        total_qty += item.quantity
        print(
            f"{item.name:<20} {item.selling_price:<10.2f} {item.quantity:<10} {subtotal:<10.2f}"
        )

    print("-" * 50)
    print(f"TOTAL: {total_qty} items | Grand Total: {total:.2f}")
