from typing import Tuple

from Data.DatabaseManager import DatabaseManager
from Data.Models import StockItem, Product
from Data.Repositories import ProductRepository
from Data.Repositories.DalModels import ProductDalModel, StockItemDalModel


class StockRepository():
    db_manager: DatabaseManager

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.db_manager.ensure_initialised()

    def get_stock_item(self, id: int) -> StockItemDalModel:
        model = StockItem.select().join(Product).where(StockItem.id == id).get()
        return StockItemDalModel.create_from_model(model)

    def get_all_stock_items(self) -> [StockItemDalModel]:
        stock_models = StockItem.select().join(Product)
        dal_models = [StockItemDalModel.create_from_model(m) for m in stock_models]

        return dal_models

    def get_stock_for_product(self, product_id: int) -> [StockItemDalModel]:
        p = Product.get_by_id(product_id)
        dal_models = [StockItemDalModel.create_from_model(m) for m in p.stock]
        return dal_models

    def get_total_product_stock(self, product_id: int) -> int:
        return Product.get_by_id(product_id).stock.count

    def edit_stock(self, stock: StockItemDalModel) -> StockItemDalModel:
        model: StockItem = StockItem.get_by_id(stock.id)
        model.quantity = stock.quantity
        model.location = stock.location
        model.save()
        return StockItemDalModel.create_from_model(model)