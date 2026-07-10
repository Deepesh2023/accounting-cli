from cli.menu import show_main_menu
from inventory.repository import InventoryRepository

inventory_repository = InventoryRepository()

show_main_menu(inventory_repository=inventory_repository)
