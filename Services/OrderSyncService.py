from time import sleep
from typing import Callable, List
from kivy.network.urlrequest import UrlRequest


class OrderApiModel:
    # {
    #    "name" : "Natalie Portman",
    #    "address" : "12 Russell Square, London",
    #    "item" : "Xiaomi Mi Note 10",
    #    "price" : 250
    # },
    name: str
    address: str
    item_name: str
    price: int
    storefront: str

    def __init__(self, name: str, address: str, item_name: str, price: int, storefront: str) -> None:
        self.name = name
        self.address = address
        self.item_name = item_name
        self.price = price
        self.storefront = storefront


OrderFetchSuccessCallback = Callable[[List[OrderApiModel], ], None]
OrderSyncCallback = Callable[[int, int, List[OrderApiModel]], None] #succeeded, failed, orders
OrderFetchErrorCallback = Callable[[object, object], None]
OrderFetcher = Callable[[OrderFetchSuccessCallback, OrderFetchErrorCallback], UrlRequest]


class Storefront:
    name: str
    fetch_orders: OrderFetcher

    def __init__(self, name: str, fetch_orders: OrderFetcher) -> None:
        self.name = name
        self.fetch_orders = fetch_orders


def fetch_webay_orders(success: OrderFetchSuccessCallback, failure: OrderFetchErrorCallback) -> UrlRequest:
    print("Beginning Fetch")

    def _success(req, result):
        orders = []
        for api_json in result:
            order = OrderApiModel(api_json["name"], api_json["address"], api_json["item"], api_json["price"], "webay")
            orders.append(order)
        success(orders)

    def _failure(req, result):
        print("WEBAY FETCH FAILED", req, result)
        failure(req, result)

    req = UrlRequest("http://localhost:8080", _success, on_failure=_failure)
    req.wait()
    return req

def fetch_test_orders(success: OrderFetchSuccessCallback, failure: OrderFetchErrorCallback) -> UrlRequest:
    sleep(3)
    success([])

webay_storefront = Storefront("webay", fetch_webay_orders)
test_storeftont = Storefront("test", fetch_test_orders)

import threading

class OrderSyncService:
    storefronts: List[Storefront]
    delay: float

    def __init__(self, stores: List[Storefront], delay: float = .1):
        self.delay = delay
        self.storefronts = stores

    def sync_orders(self, on_complete: OrderSyncCallback) -> None:
        def _thread():
            completed: int = 0
            result: List[OrderApiModel] = []
            successful: int = 0
            failed: int = 0
            expected: int = len(self.storefronts)

            def _success(new_orders: List[OrderApiModel]):
                print("success")
                nonlocal completed
                nonlocal successful
                completed += 1
                successful += 1
                result.extend(new_orders)

            def _failure(request: object, response: object):
                nonlocal completed
                nonlocal failed
                completed += 1
                failed += 1

            for store in self.storefronts:
                store.fetch_orders(_success, _failure)

            while completed < expected:
                print("SLEEPING while fetching", completed, successful, failed)
                sleep(self.delay)

            on_complete(successful, failed, result)

        x = threading.Thread(target=_thread)
        x.start()