from cli.menu import show_main_menu
from container import container

show_main_menu(
    inventory_repository=container.inventory_repository, 
    sale_repository=container.sale_repository
)
