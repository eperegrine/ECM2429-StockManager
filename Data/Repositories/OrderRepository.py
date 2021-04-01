from typing import List, Tuple

from Data.DatabaseManager import DatabaseManager
from Data.Models import Order, Product, ProductOrder
from Data.Repositories.DalModels import OrderDalModel, ProductDalModel, \
    OrderStatus, ProductOrderDalModel, PickingStatus


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

    def start_picking(self, po: ProductOrderDalModel):
        po_model = ProductOrder.get_by_id(po.id)
        po_model.picking_status = PickingStatus.InProgress.value
        po_model.save()

    def cancel_picking(self, po: ProductOrderDalModel):
        po_model = ProductOrder.get_by_id(po.id)
        po_model.picking_status = PickingStatus.NotPicked.value
        po_model.save()

    def pick_order_item(self, po: ProductOrderDalModel):
        # TODO: reduce stock levels when picked
        po_model: ProductOrder = ProductOrder.get_by_id(po.id)
        po_model.picking_status = PickingStatus.Done.value
        po_model.save()
        self._check_if_order_picked(po_model.order)

    def _check_if_order_picked(self, order: Order):
        if not order.status == OrderStatus.Picking.value:
            # Not picking so no need to check
            print("ORDER NOT PICKING, NO NEED TO CHECK")
            return
        found_unpicked = False
        for po in order.products:
            found_unpicked = not po.picking_status == PickingStatus.Done.value
            print(po.id, found_unpicked)
            if found_unpicked:
                break
        if not found_unpicked:
            print("UPDATING ORDER STATUS")
            order.status = OrderStatus.Picked.value
            order.save()
