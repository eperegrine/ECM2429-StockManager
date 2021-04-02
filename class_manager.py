"""
This module helps to avoid class instances being duplicated by providing
a registry of instantiated objects
"""
from typing import TypeVar, Generic

from Data import DatabaseManager
from Data.Repositories import StockRepository, ProductRepository, OrderRepository
from Services import OrderFetchService, webay_storefront, OrderSyncService, PrintService, MailService

_dbm = DatabaseManager()
_fetch_service = OrderFetchService([webay_storefront])
_order_repo = OrderRepository(_dbm)
_product_repo = ProductRepository(_dbm)

registry = {
    DatabaseManager: _dbm,
    # Repositories
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

    :param class_type:
    :return:
    """
    print("Getting instance of ", class_type)
    if class_type in registry:
        return registry[class_type]
    else:
        raise InstanceNotFoundError()
