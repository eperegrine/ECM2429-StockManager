from typing import Tuple

from Data.DatabaseManager import DatabaseManager
from Data.Models import ProductModel
from Data.Repositories.DalModels import ProductDalModel


def _create_product_from_row(row: Tuple) -> ProductModel:
    return ProductModel(row[1], row[2], row[3], row[0])


class ProductRepository():
    db_manager: DatabaseManager

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.db_manager.ensure_initialised()

    def get_all_products(self) -> [ProductDalModel]:
        """
        Retrieves all products from the database and converts to DAL model

        :return: A list of all products
        """
        conn = self.db_manager.get_connection()
        cur = conn.cursor()

        products = []

        for row in cur.execute('SELECT * FROM Products;'):
            model = _create_product_from_row(row)
            products.append(ProductDalModel.create_from_model(model))

        conn.close()

        return products

    def get_product(self, id: int) -> ProductDalModel:
        """
        Retrieves a product from the database with the specified id

        :param id: The id of the product to retrieve
        :return: The product
        """
        conn = self.db_manager.get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, name, description, target_level FROM Products WHERE id=?;", (id,))
        res = cur.fetchone()
        product_model = _create_product_from_row(res)
        product = ProductDalModel.create_from_model(product_model)
        conn.close()

        return product

    def create_product(self, name: str, description: str, target_stock: int) -> ProductDalModel:
        """
        Creates a product in the database and assigns an id

        :param name: The name of the product
        :param description: An explanation of the product
        :param target_stock: The ideal stock level
        :return: The new product
        """
        conn = self.db_manager.get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO Products (name, description, target_level)  VALUES 
            (?, ?, ?);
        """, (name, description, target_stock))

        id = cur.lastrowid

        product = ProductDalModel(id, name, description, target_stock)

        conn.commit()
        conn.close()

        return product

    def edit_product(self, product: ProductDalModel) -> ProductDalModel:
        """
        Updates the product in the database

        :param product: The product to update with the new values set
        :return: The new product
        """
        conn = self.db_manager.get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE Products SET name = ?, description = ?, target_level = ? WHERE id = ?;
        """, (product.name, product.description, product.target_stock, product.id))

        conn.commit()
        conn.close()

        return product

    def delete_product(self, id: int):
        """
        Deletes the specified product from the database

        :param id: The id of the product to delete
        """
        conn = self.db_manager.get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM Products WHERE id = ?;", (id,))

        conn.commit()
        conn.close()
