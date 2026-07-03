from inventory.service import show_menu as show_inventory_menu


def show_main_menu():
    print("=" * 28)
    print("Welcome to Printos accounting!")
    print("=" * 28)

    user_commands = {
        "1": "Inventory",
        "0": "exit",
    }

    while True:
        for command_key, command in user_commands.items():
            print(f"{command_key}: {command}")
            print()

        choice = input("Choice: ")

        if choice == "0":
            break

        if choice not in user_commands.keys():
            print("Invalid command.")
            continue

        if choice == "1":
            show_inventory_menu()

    print("=" * 28)
    print("Goodbye!")
    print("=" * 28)
