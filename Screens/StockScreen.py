from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

from Data import DatabaseManager
from Data.Repositories.DalModels import StockItemDalModel
from Widgets import Table, TableField, create_label_cell

from Data.Repositories import StockRepository

Builder.load_file("Screens/StockScreen.kv")

from .TableScreen import TableScreen


class QuantityTableCell(Widget):
    pass


class StockScreen(TableScreen):
    def __init__(self, **kw):
        print("Init Stock")
        self.repo = StockRepository(DatabaseManager())
        self.stock = self.repo.get_all_stock_items()
        headers = [
            TableField("ID", .2, lambda s: create_label_cell(s.id)),
            TableField("Name", .4, lambda s: create_label_cell(s.product.name)),
            TableField("Location", .2, lambda s: create_label_cell(s.location)),
            # TODO: Change to quantity table cell
            TableField("Quantity", .4, lambda s: create_label_cell(s.quantity)),
        ]
        super().__init__(headers, **kw)

    def on_kv_post(self, base_widget):
        print("Post Stock")
        super().on_kv_post(base_widget)
        self.table.setup(self.headers, self.stock)
