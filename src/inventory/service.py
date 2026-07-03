options = {
    "1": "Add product",
    "2": "Remove product",
}


def show_menu():
    while True:
        for option, description in options.items():
            print(f"{option}: {description}")

        print("0: Return")

        choice = input("Choice: ")

        if choice == "0":
            return

        if choice not in options.keys():
            print("Invalid option.")
            continue
