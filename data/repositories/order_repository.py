from typing import List, Tuple

from peewee import JOIN

from data.models import Order, Product, ProductOrder, Shipment
from data.repositories import Repository
from data.repositories.dal_models import OrderDalModel, ProductDalModel, \
    OrderStatus, ProductOrderDalModel, PickingStatus


class OrderRepository(Repository):
    def get_order(self, id: int) -> OrderDalModel:
        """
        Get an order from the database

        :param id: The id of the order to retrieve
        :return: The OrderModel
        """
        model = self._get_order_model(id)
        return OrderDalModel.create_from_model(model)

    def _get_order_model(self, id) -> Order:
        """
        Get a order database model - does not convert to DAL model
        """
        return Order.select().join(ProductOrder).where(Order.id == id).get()

    def get_all_orders(self) -> List[OrderDalModel]:
        """
        Get all orders in the database

        :return: A list of all orders in the database
        """
        orders = Order.select()
        product_orders = (ProductOrder.select())
        order_models = orders.prefetch(product_orders, (Product.select()))
        dal_models = [OrderDalModel.create_from_model(m) for m in order_models]

        return dal_models

    def create_order(self, customer_name: str, email_address: str, address: str, storefront: str,
                     products: List[Tuple[ProductDalModel, int]]) -> OrderDalModel:
        """
        Create an order in the database

        :param customer_name: The name of the customer
        :param email_address: The email address of the customer
        :param address: The address to send the order to
        :param storefront: The store the order is from
        :param products: A collection of tuples of the product and the price
        :return: The new order
        """
        o = Order(customer_name=customer_name, email_address=email_address, address=address,
                  storefront=storefront, status=OrderStatus.Pending.value)
        o.save()
        for product, price in products:
            po = ProductOrder(product_id=product.id, order=o, price=price)
            po.save()

        return OrderDalModel.create_from_model(o)

    def _simple_status_change(self, order_id, status: OrderStatus) -> Order:
        """
        A helper method to change the state

        :param order_id: The order to modify
        :param status: The new status
        :return: The order model
        """
        order = Order.get_by_id(order_id)
        order.status = status.value
        order.save()
        return order

    def _checked_status_change(self, order_id: int, status: OrderStatus, acceptable_states: List[OrderStatus]) -> Order:
        """
        A helper method to change the state if the order state is in an acceptable state

        :param order_id: The order to update
        :param status: The status to move to
        :param acceptable_states: A list of states that the order can be in before the update
        :return: The order model
        """
        o = self._get_order_model(order_id)
        if OrderStatus(o.status) in acceptable_states:
            o.status = status.value
            o.save()
        return o

    def confirm_order(self, o: OrderDalModel):
        """
        Set the state of the order to confirmed if it is pending

        :param o: The order to update
        """
        self._checked_status_change(o.id, OrderStatus.Picking, [OrderStatus.Pending])

    def start_picking(self, po: ProductOrderDalModel):
        """
        Start picking a product for an order

        :param po: The product order model
        """
        po_model = ProductOrder.get_by_id(po.id)
        po_model.picking_status = PickingStatus.InProgress.value
        po_model.save()

    def cancel_picking(self, po: ProductOrderDalModel):
        """
        Stop picking a product for an order

        :param po: The product order model
        """
        po_model = ProductOrder.get_by_id(po.id)
        po_model.picking_status = PickingStatus.NotPicked.value
        po_model.save()

    def pick_order_item(self, po: ProductOrderDalModel):
        """
        Mark a product as picked for the order, this then updates the order state

        :param po: The product order model
        """
        # TODO: reduce stock levels when picked
        po_model: ProductOrder = ProductOrder.get_by_id(po.id)
        po_model.picking_status = PickingStatus.Done.value
        po_model.save()
        self._check_if_order_picked(po_model.order)

    def _check_if_order_picked(self, order: Order):
        """
        Checks if every item of the order is picked, and if so updates the state

        :param order: The order to check
        """
        if not order.status == OrderStatus.Picking.value:
            # Not picking so no need to check
            return
        found_unpicked = False
        for po in order.products:
            found_unpicked = not po.picking_status == PickingStatus.Done.value
            if found_unpicked:
                break
        if not found_unpicked:
            order.status = OrderStatus.Picked.value
            order.save()

    def set_shipping_info(self, order_id: int, provider: str, code: str) -> OrderDalModel:
        """
        Set the shipping information - if information exists the Shipment model is modified

        :param order_id: The order to update
        :param provider: The shipping provider
        :param code: The traacking code for the order
        :return: The new order dal model
        """
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

    def mark_as_shipping(self, order_id: int):
        """
        Mark the order as shipping

        :param order_id: The id of the order to update
        """
        self._simple_status_change(order_id, OrderStatus.Shipping)

    def mark_as_shipped(self, order_id: int):
        """
        Mark the order as shipped - cannot be done unless the shipping info has been assigned

        :param order_id: The id of the order to update
        """
        order = Order.get_by_id(order_id)
        if order.shipment is None:
            raise Exception("Cannot mark as shipped without shipment info")
        order.status = OrderStatus.Shipped.value
        order.save()

    def mark_as_closed(self, order_id: int):
        """
        Close the order

        :param order_id: The id of the order
        """
        self._simple_status_change(order_id, OrderStatus.Closed)
