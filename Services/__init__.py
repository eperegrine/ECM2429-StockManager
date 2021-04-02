from typing import List

from .Models.OrderApiModel import OrderApiModel
from .Models.Storefront import Storefront, webay_storefront
from .OrderFetchService import OrderFetchService
from .OrderSyncService import OrderSyncService
from .PrintService import PrintService

storefronts: List[Storefront] = [webay_storefront]
