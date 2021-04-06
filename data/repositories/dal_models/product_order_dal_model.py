from enum import Enum

from data.models import ProductOrder
from data.repositories.dal_models import ProductDalModel


class PickingStatus(Enum):
    NotPicked = 1
    InProgress = 2
    Done = 3

    def __str__(self):
        return self.name


class ProductOrderDalModel:
    """
    A data abstraction model for product orders
    """
    id: int
    product: ProductDalModel
    price: int
    status: PickingStatus

    # order_model

    def __init__(self, id: int, product: ProductDalModel, price: int, status: PickingStatus) -> None:
        self.id = id
        self.price = price
        self.product = product
        self.status = status

    @staticmethod
    def create_from_model(model: ProductOrder):
        picking_status = PickingStatus(model.picking_status)
        return ProductOrderDalModel(model.id,
                                    ProductDalModel.create_from_model(model.product),
                                    model.price,
                                    picking_status
                                    )
