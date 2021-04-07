from threading import Thread
from time import sleep
from typing import List

from .models import OrderApiModel, Storefront
from .models.OrderFetchTyping import OrderSyncCallback


class OrderFetchService:
    """
    Handles fetching the orders from all of the storefronts
    """
    storefronts: List[Storefront]
    delay: float

    def __init__(self, stores: List[Storefront], delay: float = .1):
        self.delay = delay
        self.storefronts = stores

    def fetch_orders(self, on_complete: OrderSyncCallback) -> None:
        """
        Starts a thread to fetch orders from all storefronts

        :param on_complete: Called when all requests have completed,
        returning the number passed and failed as well as the orders
        """
        def _thread():
            completed: int = 0
            result: List[OrderApiModel] = []
            successful: int = 0
            failed: int = 0
            expected: int = len(self.storefronts)

            def _success(new_orders: List[OrderApiModel]):
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

        x = Thread(target=_thread)
        x.start()
