from typing import List, Tuple

from peewee import JOIN

from data.models import Order, Product, ProductOrder, Shipment
from data.repositories import Repository
from data.repositories.dal_models import OrderDalModel, ProductDalModel, \
    OrderStatus, ProductOrderDalModel, PickingStatus


class OrderRepository(Repository):
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

    def create_order(self, customer_name: str, email_address: str, address: str, storefront: str,
                     products: List[Tuple[ProductDalModel, int]]) -> OrderDalModel:
        o = Order(customer_name=customer_name, email_address=email_address, address=address,
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

    def set_shipping_info(self, order_id, provider, code) -> OrderDalModel:
        order = Order.select().join(Shipment, join_type=JOIN.LEFT_OUTER).where(Order.id == order_id).get()
        shipment: Shipment
        save_order = False
        if order.shipment is not None:
            shipment = order.shipment
        else:
            shipment = Shipment()
            save_order = True

        shipment.provider = provider
        shipment.tracking_code = code
        order.shipment = shipment
        shipment.save()
        if save_order:
            order.save()

        return OrderDalModel.create_from_model(order)

    def _simple_status_change(self, order_id, status: OrderStatus) -> Order:
        order = Order.get_by_id(order_id)
        order.status = status.value
        order.save()
        return order

    def mark_as_shipping(self, order_id):
        self._simple_status_change(order_id, OrderStatus.Shipping)

    def mark_as_shipped(self, order_id):
        order = Order.get_by_id(order_id)
        if order.shipment is None:
            raise Exception("Cannot mark as shipped without shipment info")
        order.status = OrderStatus.Shipped.value
        order.save()

    def mark_as_closed(self, order_id):
        self._simple_status_change(order_id, OrderStatus.Closed)
