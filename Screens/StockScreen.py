from typing import Callable

from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

from Data import DatabaseManager
from Data.Repositories.DalModels import StockItemDalModel
from Utils import BackgroundColor, BackgroundBoxLayout
from Widgets import Table, TableField, create_label_cell, ActionsTableCell

from Data.Repositories import StockRepository
from Screens.Popups import QuantityChangePopup
from Screens.TableScreen import TableScreen

Builder.load_file("Screens/StockScreen.kv")


def _create_qty_cell(si: StockItemDalModel, modify_stock_callback: Callable[[int], bool]):
    return QuantityTableCell(modify_stock_callback, si)


def _create_action_view(stock: StockItemDalModel, edit: Callable, remove: Callable) -> Widget:
    action_cell = ActionsTableCell()
    action_cell.setup(stock, edit, remove)
    return action_cell

class QuantityTableCell(BackgroundColor):
    label: Label

    remove_button: Button
    add_button: Button

    stock_item: StockItemDalModel
    modify_callback: Callable[[int], bool]

    def __init__(self, modify_callback: Callable[[int], bool], stock_item: StockItemDalModel, **kwargs):
        self.stock_item = stock_item
        self.modify_callback = modify_callback
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.remove_button = self.ids["remove_button"]
        self.label = self.ids["quantity_label"]
        self.add_button = self.ids["add_button"]

        self.add_button.on_press = self.add_qty
        self.remove_button.on_press = self.remove_qty
        self.update_text()

    def update_text(self):
        self.label.text = str(self.stock_item.quantity)
        self.remove_button.disabled = self.stock_item.quantity <= 0

    def add_qty(self):
        self.modify_callback(1)
        self.update_text()

        print("Add Quantity")

    def remove_qty(self):
        self.modify_callback(-1)
        self.update_text()


class StockScreen(TableScreen):
    stock: [StockItemDalModel]

    def __init__(self, **kw):
        self.repo = StockRepository(DatabaseManager())
        self.stock = self.repo.get_all_stock_items()
        headers = [
            TableField("ID", .1, lambda s: create_label_cell(s.id)),
            TableField("Product Name", .3, lambda s: create_label_cell(s.product.name)),
            TableField("Location", .1, lambda s: create_label_cell(s.location)),
            # TODO: Change to quantity table cell
            TableField("Quantity", .2, lambda s: _create_qty_cell(s, self.get_stock_modifier(s))),
            TableField("Actions", .3, lambda s: _create_action_view(s, self.edit_stock, self.remove_stock))
        ]
        super().__init__(headers, **kw)

    def get_stock_modifier(self, si: StockItemDalModel) -> Callable[[int], bool]:
        def modifier(amt: int):
            si.quantity += amt
            self.repo.edit_stock(si)
            return True

        return modifier

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.table.setup(self.headers, self.stock)

    def on_refresh(self):
        self.stock = self.repo.get_all_stock_items()
        self.table.set_data(self.stock)

    def edit_stock(self, stock: StockItemDalModel):
        pass

    def remove_stock(self, stock: StockItemDalModel):
        pass
