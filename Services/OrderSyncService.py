from typing import List, Callable, Dict, Tuple

from Data.Repositories import OrderRepository, ProductRepository
from Data.Repositories.DalModels import ProductDalModel
from .Models import OrderApiModel
from .OrderFetchService import OrderFetchService

# "name": ("storefront", "email", [("product", "price")])
ApiOrderDictionary = Dict[str, Tuple[str, str, List[Tuple[str, int]]]]


def group_orders_by_name(orders) -> ApiOrderDictionary:
    order_dict: ApiOrderDictionary = {}
    print(f"GOT {len(orders)} ORDERS: ", orders, )
    for api_order in orders:
        name = api_order.name
        product_tuple = (api_order.item_name, api_order.price)
        if name in order_dict:
            store, email, products = order_dict[name]
            order_dict[name] = store, email, [*products, product_tuple]
        else:
            order_dict[name] = api_order.storefront, api_order.email_address, [product_tuple]
    return order_dict


class OrderSyncService:
    fetch_service: OrderFetchService
    order_repo: OrderRepository
    product_repo: ProductRepository

    def __init__(self, fetch_service: OrderFetchService, order_repo: OrderRepository, product_repo) -> None:
        self.fetch_service = fetch_service
        self.order_repo = order_repo
        self.product_repo = product_repo

    def sync(self, on_finished: Callable):
        # This could be improved by adding batching to avoid multiple db calls
        # With multiple storefronts matching names could be an issue
        def _completed(succesful: int, failed: int, orders: List[OrderApiModel]):
            order_dict = group_orders_by_name(orders)
            print("Made order dict", order_dict)
            for name, value in order_dict.items():
                storefront, email, prod_tuple_list = value
                products: List[Tuple[ProductDalModel, int]] = [
                    (self.product_repo.get_or_create_by_name(name), price) for name, price in prod_tuple_list
                ]
                order = self.order_repo.create_order(name, email, storefront, products)
                print("Order created", order)
            print("SYNCED ORDERS")
            on_finished()

        self.fetch_service.fetch_orders(_completed)
