from typing import List

from .OrderFetchService import OrderFetchService
from .Models.Storefront import Storefront, webay_storefront
from .Models.OrderApiModel import OrderApiModel
from .OrderSyncService import OrderSyncService

storefronts: List[Storefront] = [webay_storefront]