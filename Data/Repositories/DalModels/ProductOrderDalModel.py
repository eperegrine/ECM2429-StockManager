from Data.Models import ProductOrder
from Data.Repositories.DalModels import ProductDalModel


class ProductOrderDalModel:
    """
    A data abstraction model for product orders
    """
    id: int
    product: ProductDalModel
    price: int

    # order_model

    def __init__(self, id: int, product: ProductDalModel, price: int) -> None:
        self.id = id
        self.price = price
        self.product = product

    @staticmethod
    def create_from_model(model: ProductOrder):
        return ProductOrderDalModel(model.id,
                                    ProductDalModel.create_from_model(model.product),
                                    model.price)
