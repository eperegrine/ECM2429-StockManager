import unittest
from typing import List

from services.models import OrderApiModel
from services.order_sync_service import group_orders_by_name


class OrderSyncServiceTests(unittest.TestCase):
    def test_group_orders_by_name_groups_orders(self):
        # Arrange
        storefront = "test"
        orders: List[OrderApiModel] = [
            OrderApiModel("John", "123 Fake St", "iPhone", 699, storefront),
            OrderApiModel("John", "123 Fake St", "AirPods", 170, storefront),
            OrderApiModel("Emily", "265 Fake St", "iPad", 499, storefront)
        ]

        # Act
        order_dict = group_orders_by_name(orders)

        # Assert
        self.assertEqual(2, len(order_dict))
        john_order, john_products = order_dict["John"]
        self.assertEqual(storefront, john_order.storefront)
        self.assertEqual("123 Fake St", john_order.address)
        self.assertEqual(2, len(john_products))
        self.assertEqual(("iPhone", 699), john_products[0])
        self.assertEqual(("AirPods", 170), john_products[1])
        emily_order, emily_products = order_dict["Emily"]
        self.assertEqual("265 Fake St", emily_order.address)
        self.assertEqual(storefront, emily_order.storefront)
        self.assertEqual(1, len(emily_products))
        self.assertEqual(("iPad", 499), emily_products[0])


if __name__ == '__main__':
    unittest.main()
