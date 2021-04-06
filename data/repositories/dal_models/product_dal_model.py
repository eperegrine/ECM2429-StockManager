from data.models import Product


class ProductDalModel:
    id: int
    name: str
    description: str
    target_stock: int

    def __init__(self, id, name, description, target_stock) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.target_stock = target_stock

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, ProductDalModel):
            return False
        else:
            return self.id == o.id and \
                   self.name == o.name and \
                   self.description == o.description and \
                   self.target_stock == o.target_stock

    @staticmethod
    def create_from_model(model: Product):
        return ProductDalModel(model.id, model.name, model.description, model.target_stock)
