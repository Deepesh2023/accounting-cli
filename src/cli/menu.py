from inventory.service import show_menu as show_inventory_menu

USER_COMMANDS = {
    "0": "exit",
    "1": "Inventory",
}


def show_main_menu(inventory: []):
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
            show_inventory_menu(inventory=inventory)

    print("=" * 28)
    print("Goodbye!")
    print("=" * 28)
