from peewee import *

from config import database_store

db = SqliteDatabase(str(database_store))


class BaseModel(Model):
    class Meta:
        database = db


class Product(BaseModel):
    id = AutoField()
    name = CharField()
    description = TextField()
    # target_stock = IntegerField(constraints=Check('target_stock > -1'))
    target_stock = IntegerField()

class StockItem(BaseModel):
    id = AutoField()
    product = ForeignKeyField(Product, backref="stock")
    location = CharField()
    # quantity = IntegerField(constraints=Check('quantity > -1'))
    quantity = IntegerField()

class Order(BaseModel):
    id = AutoField()
    customer_name = CharField()
    """
    TODO: use Enum 
    https://peewee.readthedocs.io/en/latest/peewee/models.html#creating-a-custom-field
    1 - Pending
    2 - Picking
    3 - Shipped
    4 - Closed
    """
    status = IntegerField()
    storefront = CharField(null=True, default="webay")
    # MAYBE? closed = bool  -> add as check method


class ProductOrder(BaseModel):
    id = AutoField()
    product = ForeignKeyField(Product, backref="orders")
    price = IntegerField()
    order = ForeignKeyField(Order, backref="products")


class Shipment(BaseModel):
    id = AutoField()
    order = ForeignKeyField(Order, backref="shipment")
    provider = CharField()
    tracking_code = CharField()


model_list = [Product, StockItem, Order, ProductOrder, Shipment]
