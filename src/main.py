from cli.menu import show_main_menu
from container import container


def cli_entry():
    show_main_menu(
        inventory_service=container.inventory_service, 
        sale_service=container.sale_service
    )


if __name__ == "__main__":
    cli_entry()
