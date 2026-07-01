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
