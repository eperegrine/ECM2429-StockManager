from typing import Tuple

from Data.DatabaseManager import DatabaseManager
from Data.Models import Product
from Data.Repositories.DalModels import ProductDalModel

class ProductRepository():
    """
    Act as a buffer between the data layer and the application layer
    """
    db_manager: DatabaseManager

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.db_manager.ensure_initialised()

    def get_all_products(self) -> [ProductDalModel]:
        """
        Retrieves all products from the database and converts to DAL model

        :return: A list of all products
        """
        products = Product.select()
        dal_models = [ProductDalModel.create_from_model(p) for p in products]
        return dal_models

    def get_product(self, id: int) -> ProductDalModel:
        """
        Retrieves a product from the database with the specified id

        :param id: The id of the product to retrieve
        :return: The product
        """
        product_model = Product.get(Product.id == id)
        product = ProductDalModel.create_from_model(product_model)
        return product

    def create_product(self, name: str, description: str, target_stock: int) -> ProductDalModel:
        """
        Creates a product in the database and assigns an id

        :param name: The name of the product
        :param description: An explanation of the product
        :param target_stock: The ideal stock level
        :return: The new product
        """
        model = Product.create(name=name, description=description, target_stock=target_stock)
        product = ProductDalModel.create_from_model(model)

        return product

    def edit_product(self, product: ProductDalModel) -> ProductDalModel:
        """
        Updates the product in the database

        :param product: The product to update with the new values set
        :return: The new product
        """

        model = Product.get(Product.id == product.id)
        model.name = product.name
        model.description = product.description
        model.target_stock = product.target_stock
        model.save()

        return ProductDalModel.create_from_model(model)

    def delete_product(self, id: int):
        """
        Deletes the specified product from the database

        :param id: The id of the product to delete
        """
        model = Product.get(Product.id == id)
        model.delete_instance()