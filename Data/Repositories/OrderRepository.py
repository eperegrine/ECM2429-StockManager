from Data.DatabaseManager import DatabaseManager
from Data.Models import Order, Product, ProductOrder
from Data.Repositories.DalModels import OrderDalModel


class OrderRepository:
    db_manager: DatabaseManager

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.db_manager.ensure_initialised()

    def get_order(self, id: int) -> OrderDalModel:
        model = Order.select().join(ProductOrder).where(Order.id == id).get()
        return OrderDalModel.create_from_model(model)

    def get_all_orders(self) -> [OrderDalModel]:
        orders = Order.select()
        product_orders = (ProductOrder.select())
        order_models = orders.prefetch(product_orders, (Product.select()))
        dal_models = [OrderDalModel.create_from_model(m) for m in order_models]

        return dal_models