from OrderSyncService import OrderSyncService, OrderApiModel, webay_storefront

if __name__ == '__main__':
    sync_service = OrderSyncService([webay_storefront])
    sync_service.sync_orders()