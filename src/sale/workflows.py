import uuid
from typing import List, Optional
from sale.models import Sale, SaleItem
from sale.service import SaleService
from inventory.service import InventoryService
from shared.utils import get_input, get_confirmation, display_table

SALE_MENU_OPTIONS = {
    "1": "Record a sale",
    "2": "View sale history",
    "3": "View sale detail",
}

def show_menu(sale_service: SaleService, inventory_service: InventoryService):
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
            record_sale_workflow(inventory_service, sale_service)
        
        if choice == "2":
            view_sales_history(sale_service)
        
        if choice == "3":
            view_sale_detail_workflow(sale_service)

def record_sale_workflow(inventory_service: InventoryService, sale_service: SaleService):
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
        print("5: Search for product ID")
        print("0: Cancel and return")

        choice = input("Choice: ")

        if choice == "0":
            print("Sale cancelled.")
            return

        if choice == "5":
            from inventory.workflows import search_product_workflow
            search_product_workflow(inventory_service)
            continue

        if choice == "1":
            item = add_item_to_list(inventory_service)
            if item:
                existing = next(
                    (si for si in selling_items if si.product_id == item.product_id and si.selling_price == item.selling_price),
                    None,
                )
                if existing:
                    existing.quantity += item.quantity
                else:
                    selling_items.append(item)

        elif choice == "2":
            remove_item_from_list(selling_items)

        elif choice == "3":
            edit_item_in_list(selling_items, inventory_service)

        elif choice == "4":
            if not selling_items:
                print("Sale must contain at least one item.")
                continue

            if get_confirmation("Confirm this sale?"):
                sale_service.record_sale(items=selling_items)
                print("\nSale recorded successfully!")
                return
            else:
                print("\nConfirmation cancelled.")
        else:
            print("Invalid option.")

def add_item_to_list(inventory_service: InventoryService) -> Optional[SaleItem]:
    product_id_str = get_input("Enter Product ID: ", str)
    try:
        product_id = uuid.UUID(product_id_str)
    except ValueError:
        print("Invalid UUID format.")
        return None

    try:
        product = inventory_service.get_product(product_id)
    except Exception:
        print("Product not found or archived.")
        return None

    print(f"Selected: {product.name} | Price: {product.selling_price} | Stock: {product.quantity}")

    price_input = get_input(f"Selling Price [{product.selling_price}]: ", float)
    price = price_input if price_input is not None else product.selling_price

    quantity_input = get_input(f"Quantity [{product.quantity}]: ", int)
    quantity = quantity_input if quantity_input is not None else 1

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

def edit_item_in_list(selling_items: List[SaleItem], inventory_service: InventoryService):
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
    try:
        product = inventory_service.get_product(item.product_id)
    except Exception:
        product = None

    price_input = get_input(f"New Price [{item.selling_price}]: ", float)
    price = price_input if price_input is not None else item.selling_price

    quantity_input = get_input(f"New Quantity [{item.quantity}]: ", int)
    quantity = quantity_input if quantity_input is not None else item.quantity

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

def view_sales_history(sale_service: SaleService):
    sales = sale_service.list_sales()
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
    header = f"{'Item':<20} {'Price':<10} {'Qty':<10} {'Subtotal':<10}"
    rows = []
    total = 0
    total_qty = 0
    for item in items:
        subtotal = item.selling_price * item.quantity
        total += subtotal
        total_qty += item.quantity
        rows.append(f"{item.name:<20} {item.selling_price:<10.2f} {item.quantity:<10} {subtotal:<10.2f}")
    
    footer = f"TOTAL: {total_qty} items | Grand Total: {total:.2f}"
    display_table(header, rows, footer)

def view_sale_detail_workflow(sale_service: SaleService):
    sale_id_str = get_input("Enter Sale ID to view details: ", str)
    try:
        sale_id = uuid.UUID(sale_id_str)
    except ValueError:
        print("Invalid UUID format.")
        return

    try:
        sale = sale_service.get_sale(sale_id)
    except ValueError as e:
        print(e)
        return

    print(f"\n--- Sale Details ---")
    print(f"Sale ID: {sale.sale_id}")
    print(f"Date: {sale.date}")
    print(f"Customer: {sale.customer_name or 'N/A'}")
    
    header = f"{'Item':<20} {'Price':<10} {'Qty':<10} {'Subtotal':<10}"
    rows = []
    total = 0
    total_qty = 0
    for item in sale.items:
        subtotal = item.selling_price * item.quantity
        total += subtotal
        total_qty += item.quantity
        rows.append(f"{item.name:<20} {item.selling_price:<10.2f} {item.quantity:<10} {subtotal:<10.2f}")
    
    footer = f"TOTAL: {total_qty} items | Grand Total: {total:.2f}"
    display_table(header, rows, footer)
