from enum import Enum
from typing import List, Optional

from Data.Models import Order
from Data.Repositories.DalModels import ProductOrderDalModel, ShipmentDalModel


class OrderStatus(Enum):
    # Not yet confirmed
    Pending = 1
    # In the process of picking
    Picking = 2
    # All items are picked in box
    Picked = 4
    # Preparing to be dispatched
    Shipping = 5
    # Sent to shipping company
    Shipped = 6
    # Received all okay
    Closed = 7

    def __str__(self):
        return self.name


class OrderDalModel:
    id: int
    customer_name: str
    email_address: str
    address: str
    status: OrderStatus
    storefront: str
    products: List[ProductOrderDalModel]
    shipment: Optional[ShipmentDalModel]

    def __init__(self, id: int, customer_name: str, email_address: str, address: str, status: OrderStatus,
                 storefront: str, products: [ProductOrderDalModel], shipment: Optional[ShipmentDalModel]) -> None:
        self.id = id
        self.customer_name = customer_name
        self.email_address = email_address
        self.address = address
        self.status = status
        self.storefront = storefront
        self.products = products
        self.shipment = shipment

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, OrderDalModel):
            return False
        else:
            # TODO: compare each product to check match
            return self.id == o.id and \
                   self.customer_name == o.customer_name and \
                   self.email_address == o.email_address and \
                   self.address == o.address and \
                   self.status == o.status and \
                   self.storefront == o.storefront and \
                   len(self.products) == len(o.products)

    @staticmethod
    def create_from_model(model: Order):
        products = [ProductOrderDalModel.create_from_model(po) for po in model.products]
        order_status = OrderStatus(model.status)
        shipment = ShipmentDalModel.create_from_model(model.shipment) if model.shipment is not None else None
        return OrderDalModel(model.id, model.customer_name, model.email_address, model.address, order_status,
                             model.storefront, products, shipment)
