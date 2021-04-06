from peewee import DoesNotExist

from data.models import StockItem, Product
from data.repositories import Repository
from data.repositories.dal_models import StockItemDalModel


class StockRepository(Repository):
    """
    A class to store, retrieve and modify stock
    """

    def get_stock_item(self, id: int) -> StockItemDalModel:
        """
        Retrieves a stock item from the database with the specified id

        :param id: The id of the stock item to retrieve
        :return: The stock item
        """
        model = StockItem.select().join(Product).where(StockItem.id == id).get()
        return StockItemDalModel.create_from_model(model)

    def get_all_stock_items(self) -> [StockItemDalModel]:
        """
        Retrieves all stock items from the database and converts to DAL model

        :return: A list of all stock items
        """
        stock_models = StockItem.select().join(Product)
        dal_models = [StockItemDalModel.create_from_model(m) for m in stock_models]

        return dal_models

    def get_stock_for_product(self, product_id: int) -> [StockItemDalModel]:
        """
        Gets all of the stock items for the specified product

        :param product_id: The id of the product
        :return: List of products stock
        """
        p = Product.get_by_id(product_id)
        dal_models = [StockItemDalModel.create_from_model(m) for m in p.stock]
        return dal_models

    def get_total_product_stock(self, product_id: int) -> int:
        """
        Gets a count of all stock stored for a product

        :param product_id: The id of the product
        :return: The total stock stored
        """
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

        try:
            stock_item = StockItem.select().where(StockItem.product_id == product_id,
                                                  StockItem.location == location).get()

            stock_item.quantity = qty
            stock_item.save()
        except DoesNotExist:
            stock_item = StockItem.create(location=location, quantity=qty, product=product)

        return StockItemDalModel.create_from_model(stock_item)

    def edit_stock(self, stock: StockItemDalModel) -> StockItemDalModel:
        """
        Updates the stock item quantity and location in the database

        :param stock: The stock item withe the new values
        :return: An updated stock item dal model
        """
        model: StockItem = StockItem.get_by_id(stock.id)
        model.quantity = stock.quantity
        model.location = stock.location
        model.save()
        return StockItemDalModel.create_from_model(model)

    def remove_item(self, stock_id):
        """
        Removes the stock item from the database

        :param id: The id of the item to remove
        """
        model: StockItem = StockItem.get_by_id(stock_id)
        model.delete_instance()
