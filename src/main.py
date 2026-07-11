from cli.menu import show_main_menu
from inventory.repository import InventoryRepository
from sale.repository import SaleRepository

inventory_repository = InventoryRepository()
sale_repository = SaleRepository()

show_main_menu(inventory_repository=inventory_repository, sale_repository=sale_repository)
