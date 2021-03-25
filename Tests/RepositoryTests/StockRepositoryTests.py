import unittest
from functools import wraps
from unittest.mock import Mock, MagicMock

from peewee import SqliteDatabase

from Data import DatabaseManager
from Data.Repositories import StockRepository
from Data.Repositories.DalModels import ProductDalModel, StockItemDalModel

from Data.Models import StockItem, Product

from .DbTestUtils import with_test_db

class StockRepositoryTests(unittest.TestCase):

    @with_test_db((Product, StockItem))
    def test_get_stock_item_returns_stock_item(self):
        repo = StockRepository(DatabaseManager())

        db_product = Product(name="iPhone X", description="Apple iPhone\nwith FaceID", target_stock=3)
        db_product.save()

        db_stock = StockItem(location="A3", quantity=4, product=db_product)
        db_stock.save()

        expected = StockItemDalModel(db_stock.id, db_stock.location, db_stock.quantity, db_product.id)
        expected.product = ProductDalModel(db_product.id, db_product.name,
                                           db_product.description, db_product.target_stock)

        #Act
        stock_item: StockItemDalModel = repo.get_stock_item(db_stock.id)

        #Assert
        self.assertEqual(stock_item, expected)

if __name__ == '__main__':
    unittest.main()
