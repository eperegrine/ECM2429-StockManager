from typing import List

from .OrderSyncService import OrderSyncService
from .Models.Storefront import Storefront, webay_storefront
from .Models.OrderApiModel import OrderApiModel

storefronts: List[Storefront] = [webay_storefront]