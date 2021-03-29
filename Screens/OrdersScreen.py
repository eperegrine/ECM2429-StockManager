from typing import Callable

from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

from Data import DatabaseManager
from Data.Repositories.DalModels import StockItemDalModel, OrderDalModel
from Data.Repositories.OrderRepository import OrderRepository
from Screens.Popups import EditStockItemPopup, AddStockItemPopup
from BackgroundColor import BackgroundColor, BackgroundBoxLayout
from Widgets import Table, TableField, create_label_cell, ActionsTableCell

from Data.Repositories import StockRepository
from Screens.Popups import QuantityChangePopup
from Screens.TableScreen import TableScreen

Builder.load_file("Screens/OrdersScreen.kv")


def _create_products_cell(o: OrderDalModel):
    prod_names = [p.product.name for p in o.products]
    return create_label_cell(", ".join(prod_names))


class OrdersScreen(TableScreen):
    orders: [OrderDalModel]

    def __init__(self, **kw):
        self.repo = OrderRepository(DatabaseManager())
        self.orders = self.repo.get_all_orders()
        headers = [
            TableField("ID", .1, lambda o: create_label_cell(o.id)),
            TableField("Customer Name", .2, lambda o: create_label_cell(o.customer_name)),
            TableField("Status", .1, lambda o: create_label_cell(o.status)),
            TableField("Store", .1, lambda o: create_label_cell(o.storefront)),
            TableField("Products", .2, lambda o: _create_products_cell(o))
            # TableField("Actions", .3, lambda s: _create_action_view(s, self.edit_stock, self.remove_stock))
        ]
        super().__init__(headers, **kw)

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.table.setup(self.headers, self.orders)

    def on_refresh(self):
        pass

    def on_add(self):
        pass
