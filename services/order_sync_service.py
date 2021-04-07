from typing import List, Callable, Dict, Tuple

from data.repositories import OrderRepository, ProductRepository
from data.repositories.dal_models import ProductDalModel
from .models import OrderApiModel
from .order_fetch_service import OrderFetchService

# "name": ("storefront", "email", [("product", "price")])
ApiOrderDictionary = Dict[str, Tuple[OrderApiModel, List[Tuple[str, int]]]]


def group_orders_by_name(orders: List[OrderApiModel]) -> ApiOrderDictionary:
    """
    Takes a list of orders and groups them by the customer

    :param orders: The list of api orders
    :return: The order products grouped by customer
    """
    order_dict: ApiOrderDictionary = {}
    for api_order in orders:
        name = api_order.name
        product_tuple = (api_order.item_name, api_order.price)
        if name in order_dict:
            api_model, products = order_dict[name]
            order_dict[name] = api_model, [*products, product_tuple]
        else:
            order_dict[name] = api_order, [product_tuple]
    return order_dict


class OrderSyncService:
    """
    Handles syncing storefront data with applications
    """
    fetch_service: OrderFetchService
    order_repo: OrderRepository
    product_repo: ProductRepository

    def __init__(self, fetch_service: OrderFetchService, order_repo: OrderRepository, product_repo) -> None:
        self.fetch_service = fetch_service
        self.order_repo = order_repo
        self.product_repo = product_repo

    def sync(self, on_finished: Callable):
        """
        Update the database from the api

        :param on_finished: A callback called when the sync has finished
        """
        # This could be improved by adding batching to avoid multiple db calls
        # With multiple storefronts matching names could be an issue
        def _completed(succesful: int, failed: int, orders: List[OrderApiModel]):
            order_dict = group_orders_by_name(orders)
            for name, value in order_dict.items():
                api_order, prod_tuple_list = value
                products: List[Tuple[ProductDalModel, int]] = [
                    (self.product_repo.get_or_create_by_name(name), price) for name, price in prod_tuple_list
                ]
                order = self.order_repo.create_order(name, api_order.email_address, api_order.address,
                                                     api_order.storefront, products)
            on_finished()

        self.fetch_service.fetch_orders(_completed)
