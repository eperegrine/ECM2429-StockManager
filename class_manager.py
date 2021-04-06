"""
This module helps to avoid class instances being duplicated by providing
a registry of instantiated objects
"""
from typing import TypeVar, Generic

from data import DatabaseManager
from data.repositories import StockRepository, ProductRepository, OrderRepository
from Services import OrderFetchService, webay_storefront, OrderSyncService, PrintService, MailService

_dbm = DatabaseManager()
_fetch_service = OrderFetchService([webay_storefront])
_order_repo = OrderRepository(_dbm)
_product_repo = ProductRepository(_dbm)

registry = {
    DatabaseManager: _dbm,
    # repositories
    StockRepository: StockRepository(_dbm),
    ProductRepository: _product_repo,
    OrderRepository: _order_repo,
    # Services
    OrderFetchService: _fetch_service,
    OrderSyncService: OrderSyncService(_fetch_service, _order_repo, _product_repo),
    PrintService: PrintService(),
    MailService: MailService()
}


class InstanceNotFoundError(Exception):
    pass


T = TypeVar('T')


def get_instance(class_type: Generic[T]) -> T:
    """
    Fetches an instance

    :param class_type: The type of the class to fetch
    :return: An instance of the specified type
    """
    print("Getting instance of ", class_type)
    if class_type in registry:
        return registry[class_type]
    else:
        raise InstanceNotFoundError()
