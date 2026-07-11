from inventory.repository import InventoryRepository
from sale.repository import SaleRepository
from shared.interfaces import InventoryRepositoryProtocol, SaleRepositoryProtocol

class Container:
    """
    A simple Dependency Container.
    Its only job is to know HOW to create the objects the app needs.
    """
    def __init__(self):
        # We instantiate the concrete implementations here
        self.inventory_repository: InventoryRepositoryProtocol = InventoryRepository()
        self.sale_repository: SaleRepositoryProtocol = SaleRepository()

# Create a single instance of the container to be used across the app
container = Container()
