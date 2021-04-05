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


class Shipment(BaseModel):
    id = AutoField()
    provider = CharField()
    tracking_code = CharField()


class Order(BaseModel):
    id = AutoField()
    customer_name = CharField()
    address = TextField()
    email_address = CharField()
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
    shipment = ForeignKeyField(Shipment, null=True, unique=True, backref="order")


class ProductOrder(BaseModel):
    id = AutoField()
    product = ForeignKeyField(Product, backref="orders")
    price = IntegerField()
    picking_status = IntegerField(default=1)
    order = ForeignKeyField(Order, backref="products")


model_list = [Product, StockItem, Order, ProductOrder, Shipment]
