from inventory.repository import InventoryRepository
from sale.repository import SaleRepository
from inventory.service import InventoryService
from sale.service import SaleService
from shared.interfaces import InventoryRepositoryProtocol, SaleRepositoryProtocol

class Container:
    """
    A simple Dependency Container.
    Its only job is to know HOW to create the objects the app needs.
    """
    def __init__(self):
        # 1. Repositories (The bottom layer)
        self.inventory_repository: InventoryRepositoryProtocol = InventoryRepository()
        self.sale_repository: SaleRepositoryProtocol = SaleRepository()

        # 2. Services (The business layer - injected with repositories)
        self.inventory_service = InventoryService(self.inventory_repository)
        self.sale_service = SaleService(self.sale_repository, self.inventory_repository)

# Create a single instance of the container to be used across the app
container = Container()
