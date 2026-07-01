print("=" * 28)
print("Welcome to Printos accounting!")
print("=" * 28)

user_commands = {
    "1": {
        "command": "Inventory",
        "options": {
            "1": "Add product",
            "2": "List product",
            "0": "Return",
        },
    },
    "0": {"command": "exit"},
}

while True:
    for choice, data in user_commands.items():
        print(f"{choice}: {data['command']}")
        print()

    choice = input("Choice: ")

    if choice == "0":
        break

    if choice in user_commands.keys():
        while True:
            for choice, data in user_commands[choice]["options"].items():
                print(f"{choice}: {data}")
                print()

            choice = input("Choice: ")
            if choice == "0":
                break

print("=" * 28)
print("Goodbye!")
print("=" * 28)
