from cli.menu import show_main_menu
from container import container

show_main_menu(
    inventory_service=container.inventory_service, 
    sale_service=container.sale_service
)
