from typing import Callable, List, Any

from Services.Models import OrderApiModel

OrderFetchSuccessCallback = Callable[[List[OrderApiModel], ], None]
OrderSyncCallback = Callable[[int, int, List[OrderApiModel]], None]  # succeeded, failed, orders
OrderFetchErrorCallback = Callable[[object, object], None]
OrderFetcher = Callable[[OrderFetchSuccessCallback, OrderFetchErrorCallback], Any]
