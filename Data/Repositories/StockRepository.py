from typing import Tuple

from Data.DatabaseManager import DatabaseManager
from Data.Models import StockItemModel
from Data.Repositories import ProductRepository
from Data.Repositories.DalModels import ProductDalModel, StockItemDalModel


def _create_stock_item_from_row(row: Tuple) -> StockItemModel:
    return StockItemModel(row[0], row[1], row[2], row[3])


class StockRepository():
    db_manager: DatabaseManager
    product_repo: ProductRepository

    def __init__(self, db_manager: DatabaseManager, product_repo: ProductRepository):
        self.db_manager = db_manager
        self.db_manager.ensure_initialised()
        self.product_repo = product_repo

    def get_stock_item(self, id: int) -> StockItemDalModel:
        con = self.db_manager.get_connection()
        cur = con.cursor()
        cur.execute("SELECT id, location, quantity, product_id FROM StockItems WHERE id=?;", (id,))
        res = cur.fetchone()
        model = _create_stock_item_from_row(res)
        dal_model = StockItemDalModel.create_from_model(model, self.product_repo)
        con.commit()
        con.close()

        return dal_model

    def get_all_stock_items(self) -> [StockItemDalModel]:
        con = self.db_manager.get_connection()
        cur = con.cursor()
        stock_items=[]
        for row in cur.execute("SELECT id, location, quantity, product_id FROM StockItems"):
            model = _create_stock_item_from_row(row)
            dal_model = StockItemDalModel.create_from_model(model, self.product_repo)
            stock_items.append(dal_model)
        con.commit()
        con.close()

        return stock_items

    def get_stock_for_product(self, product_id: int) -> [StockItemDalModel]:
        con = self.db_manager.get_connection()
        cur = con.cursor()
        stock_items=[]
        result = cur.execute("""
            SELECT id, location, quantity, product_id FROM StockItems
            WHERE product_id = ?
        """, (product_id,))

        for row in result:
            model = _create_stock_item_from_row(row)
            dal_model = StockItemDalModel.create_from_model(model, self.product_repo)
            stock_items.append(dal_model)
        con.commit()
        con.close()

        return stock_items

    def get_total_product_stock(self, product_id: int):
        stock = self.get_stock_for_product(product_id)
        #TODO: count in db
        total = 0
        for si in stock:
            total += si.quantity

        return total
