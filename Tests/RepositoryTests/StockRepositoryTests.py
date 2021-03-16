import unittest
from unittest.mock import Mock, MagicMock

from sqlite3 import Cursor, Connection
from Data import DatabaseManager
from Data.Repositories import ProductRepository, StockRepository
from Data.Repositories.DalModels import ProductDalModel, StockItemDalModel


class StockRepositoryTests(unittest.TestCase):
    def setUp(self):
        dbm = Mock(DatabaseManager)
        con = Mock(Connection)
        self.mock_cursor = Mock(Cursor)
        con.cursor = MagicMock(return_value=self.mock_cursor)
        dbm.get_connection = MagicMock(return_value=con)

        self.db_manager = dbm
        self.mock_product_repo = Mock(ProductRepository)
        self.stock_repo = StockRepository(dbm, self.mock_product_repo)

    """
    Methods every test must mock
    The database call:
    <row> = (id: int, location: str, quantity: int, product_id: int)
     - for single item: mock_cursor.fetchone() returns <row>
     - for multiple items: mock_cursor.execute(query, params) list[<row>]
    mock_product_repo.get_product(id) - get a product
    """

    # def assertStockItem(self, result, expected):
    #     self.assertEqual(result.id, id)
    #     self.assertEqual(result.location, location)
    #     self.assertEqual(result.quantity, quantity)
    #     self.assertEqual(result.product_id, product_id)
    #     self.assertEqual(result.product.id, product_id)
    #     self.assertEqual(result.product.name, product.name)
    #     self.assertEqual(result.product.description, product.description)
    #     self.assertEqual(result.product.target_stock, product.target_stock)

    def test_get_stock_item_returns_stock_item(self):
        #Arrange
        id, location, quantity, product_id = (1, "A4", 4, 2)
        product = ProductDalModel(product_id, "iPhone", "an iphone", 3)
        stock_row = (id, location, quantity, product_id)
        stock_item = StockItemDalModel(id, location, quantity, product_id)
        stock_item.product = product

        self.mock_cursor.fetchone = MagicMock(return_value=stock_row)
        self.mock_product_repo.get_product = MagicMock(return_value=product)

        #Act
        result = self.stock_repo.get_stock_item(id)

        #Assert
        self.assertEqual(result, stock_item)

if __name__ == '__main__':
    unittest.main()
