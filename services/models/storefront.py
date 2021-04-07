from kivy.network.urlrequest import UrlRequest

from .order_api_model import OrderApiModel
from .OrderFetchTyping import OrderFetcher, OrderFetchSuccessCallback, OrderFetchErrorCallback


class Storefront:
    """
    A model representing a storefront
    """
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


webay_storefront = Storefront("webay", fetch_webay_orders)
