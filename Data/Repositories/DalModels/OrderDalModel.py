from Data.Models import Order
from Data.Repositories.DalModels import ProductOrderDalModel, ProductDalModel


class OrderDalModel:
    id: int
    customer_name: str
    status: int
    storefront: str
    products: [ProductOrderDalModel]

    def __init__(self, id: int, customer_name: str, status: int, storefront: str,
                 products: [ProductOrderDalModel]) -> None:
        self.id = id
        self.customer_name = customer_name
        self.status = status
        self.storefront = storefront
        self.products = products

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, OrderDalModel):
            return False
        else:
            # TODO: compare each product to check match
            return self.id == o.id and \
                   self.customer_name == o.customer_name and \
                   self.status == o.status and \
                   self.storefront == o.storefront and \
                   len(self.products) == len(o.products)

    @staticmethod
    def create_from_model(model: Order):
        products = [ProductOrderDalModel.create_from_model(po) for po in model.products]
        return OrderDalModel(model.id, model.customer_name, model.status, model.storefront, products)
