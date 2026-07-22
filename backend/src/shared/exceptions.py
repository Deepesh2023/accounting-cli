class InventoryError(Exception):
    """Base exception for inventory related errors"""
    pass

class ProductNotFoundError(InventoryError):
    """Raised when a product is not found in the repository"""
    pass

class InvalidProductDataError(InventoryError):
    """Raised when product data is invalid (e.g. negative price)"""
    pass
