import unittest

from Data import DatabaseManager
from Data.Models import Product
from Data.Repositories import ProductRepository
from Data.Repositories.DalModels import ProductDalModel
from .DbTestUtils import with_test_db


class ProductRepositoryTests(unittest.TestCase):
    @with_test_db((Product,))
    def test_add_product_creates_product(self):
        # Arrange
        repo = ProductRepository(DatabaseManager())
        name, description, target_stock = "A", "B", 2
        expected = ProductDalModel(1, name, description, target_stock)

        # Act
        prod = repo.create_product(name, description, target_stock)

        # Assert
        self.assertEqual(prod.name, name)
        self.assertEqual(prod.description, description)
        self.assertEqual(prod.target_stock, target_stock)


if __name__ == '__main__':
    unittest.main()
