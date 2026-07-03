from inventory.service import show_menu as show_inventory_menu

USER_COMMANDS = {
    "1": "Inventory",
    "0": "exit",
}


def show_main_menu():
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

        if choice == "1":
            show_inventory_menu()

    print("=" * 28)
    print("Goodbye!")
    print("=" * 28)
