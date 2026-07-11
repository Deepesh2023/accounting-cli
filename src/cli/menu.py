from inventory.workflows import show_menu as show_inventory_menu
from sale.workflows import show_menu as show_sale_menu
from shared.interfaces import InventoryRepositoryProtocol, SaleRepositoryProtocol


USER_COMMANDS = {
    "0": "exit",
    "1": "Inventory",
    "2": "Sales",
}


def show_main_menu(inventory_service, sale_service):
    print("=" * 28)
    print("Welcome to Printos accounting!")
    print("=" * 28)

    while True:
        for command_key, command in USER_COMMANDS.items():
            print(f"{command_key}: {command}")
            print()

        choice = input("Choice: ")

        if choice == "0":
            break

        if choice not in USER_COMMANDS.keys():
            print("Invalid command.")
            continue

        print("0: Return")
        if choice == "1":
            show_inventory_menu(inventory_service)
        if choice == "2":
            show_sale_menu(sale_service, inventory_service)

    print("=" * 28)
    print("Goodbye!")
    print("=" * 28)
