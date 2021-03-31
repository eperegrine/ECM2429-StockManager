"""
This module helps to avoid class instances being duplicated by providing
a registry of instantiated objects
"""
from typing import Any, TypeVar, Generic

from Data import DatabaseManager
from Data.Repositories import StockRepository, ProductRepository, OrderRepository
from Services import OrderSyncService, webay_storefront

dbm = DatabaseManager()

registry = {
    DatabaseManager: dbm,
    # Repositories
    StockRepository: StockRepository(dbm),
    ProductRepository: ProductRepository(dbm),
    OrderRepository: OrderRepository(dbm),
    # Services
    OrderSyncService: OrderSyncService([webay_storefront])
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
