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

    def create_stock(self, product_id: int, location: str, qty: int) -> StockItemDalModel:
        """
        Creates stock but first checks for existing items to avoid duplicates

        :param product_id: The id of the product to use
        :param location: The location within the warehouse
        :param qty: The number of product at the location
        :return: The stock DAL model
        """
        product = Product.get_by_id(product_id)
        if product is None:
            raise Exception("Product cannot be None when creating stock")
        stock_item = StockItem.select().where(StockItem.product_id == product_id,
                                              StockItem.location == location).get()
        if stock_item:
            stock_item.quantity = qty
            stock_item.save()
        else:
            stock_item = StockItem.create(location=location, quantity=qty, product=product)

        return StockItemDalModel.create_from_model(stock_item)

    def edit_stock(self, stock: StockItemDalModel) -> StockItemDalModel:
        model: StockItem = StockItem.get_by_id(stock.id)
        model.quantity = stock.quantity
        model.location = stock.location
        model.save()
        return StockItemDalModel.create_from_model(model)

    def remove_item(self, stock_id):
        model: StockItem = StockItem.get_by_id(stock_id)
        model.delete_instance()
