from Data.Models import ProductModel


class ProductDalModel():
    id: int
    name: str
    description: str
    target_stock: int

    def __init__(self, id, name, description, target_stock) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.target_stock = target_stock

    @staticmethod
    def create_from_model(model: ProductModel):
        return ProductDalModel(model.id, model.name, model.description, model.target_stock)
