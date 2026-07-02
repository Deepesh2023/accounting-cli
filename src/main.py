print("=" * 28)
print("Welcome to Printos accounting!")
print("=" * 28)

user_commands = {
    "1": "Inventory",
    "0": "exit",
}

options = {
    "1": "Add product",
    "2": "Remove product",
}

while True:
    for choice, data in user_commands.items():
        print(f"{choice}: {data['command']}")
        print()

    choice = input("Choice: ")

    if choice == "0":
        break

    if choice not in user_commands.keys():
        print("Invalid command.")
        continue


print("=" * 28)
print("Goodbye!")
print("=" * 28)
