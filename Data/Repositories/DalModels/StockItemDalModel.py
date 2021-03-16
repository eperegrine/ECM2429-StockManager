from Data.Models import StockItemModel
from Data.Repositories import ProductRepository
from Data.Repositories.DalModels import ProductDalModel


class StockItemDalModel():
    id: int
    product_id: int
    location: str
    quantity: int
    product: ProductDalModel

    def __init__(self, id: int, location: str, quantity: int, product_id: int):
        self.id = id
        self.location = location
        self.quantity = quantity
        self.product_id = product_id

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, StockItemDalModel):
            return False
        else:
            return self.id == o.id and \
                   self.location == o.location and \
                   self.quantity == o.quantity and \
                   self.product_id == o.product_id and \
                   self.product == o.product

    @staticmethod
    def create_from_model(model: StockItemModel, product_repo: ProductRepository):
        dal_model = StockItemDalModel(model.id, model.location, model.quantity, model.product_id)
        product = product_repo.get_product(model.product_id)
        dal_model.product = product
        return dal_model
