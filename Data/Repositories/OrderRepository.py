from typing import List, Tuple

from Data.DatabaseManager import DatabaseManager
from Data.Models import Order, Product, ProductOrder
from Data.Repositories.DalModels import OrderDalModel, ProductDalModel, OrderStatus


class OrderRepository:
    db_manager: DatabaseManager

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.db_manager.ensure_initialised()

    def get_order(self, id: int) -> OrderDalModel:
        model = self._get_order_model(id)
        return OrderDalModel.create_from_model(model)

    def _get_order_model(self, id) -> Order:
        return Order.select().join(ProductOrder).where(Order.id == id).get()

    def get_all_orders(self) -> [OrderDalModel]:
        orders = Order.select()
        product_orders = (ProductOrder.select())
        order_models = orders.prefetch(product_orders, (Product.select()))
        dal_models = [OrderDalModel.create_from_model(m) for m in order_models]

        return dal_models

    def create_order(self, customer_name: str, email_address: str, storefront: str,
                     products: List[Tuple[ProductDalModel, int]]) -> OrderDalModel:
        o = Order(customer_name=customer_name, email_address=email_address,
                  storefront=storefront, status=OrderStatus.Pending.value)
        o.save()
        for product, price in products:
            po = ProductOrder(product_id=product.id, order=o, price=price)
            po.save()

        return OrderDalModel.create_from_model(o)

    def confirm_order(self, o: OrderDalModel):
        o = self._get_order_model(o.id)
        if o.status == OrderStatus.Pending.value:
            o.status = OrderStatus.Picking.value
            o.save()
