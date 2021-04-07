from typing import List

from .models.order_api_model import OrderApiModel
from .models.storefront import Storefront, webay_storefront
from .order_fetch_service import OrderFetchService
from .order_sync_service import OrderSyncService
from .print_service import PrintService
from .mail_service import MailService

storefronts: List[Storefront] = [webay_storefront]
