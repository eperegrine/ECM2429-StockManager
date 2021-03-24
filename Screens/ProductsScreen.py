from typing import Callable

from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView

from Screens.Popups.AddProductPopup import AddProductPopup, EditProductPopup
from Widgets import Table, TableField

Builder.load_file("Screens/ProductsScreen.kv")

from Data.Repositories.DalModels import ProductDalModel
from Data.Repositories import ProductRepository
from Data import DatabaseManager

from Utils import BackgroundLabel


def _create_label(text) -> Widget:
    lbl = BackgroundLabel()
    lbl.text = str(text)
    lbl.max_lines = 2
    return lbl


def _create_desc_label(text) -> Widget:
    # TODO: Improve multiple line handling
    return _create_label(text)


def _create_action_view(product: ProductDalModel, edit: Callable, remove: Callable) -> Widget:
    action_cell = ProductActionsTableCell()
    action_cell.setup(product, edit, remove)
    return action_cell


class ProductActionsTableCell(Widget):
    edit_btn: Button
    remove_btn: Button
    product: ProductDalModel

    def on_kv_post(self, base_widget):
        self.edit_btn = self.ids["edit_button"]
        self.remove_btn = self.ids["remove_button"]

    def setup(self, product: ProductDalModel, edit: Callable, remove: Callable):
        self.product = product
        self.edit_btn.on_press = lambda: edit(product)
        self.remove_btn.on_press = lambda: remove(product)


class ProductsScreen(Screen):
    table: Table
    add_button: Button
    refresh_button: Button

    products: [ProductDalModel]

    repo: ProductRepository

    headers: [TableField]

    def on_kv_post(self, base_widget):
        self.table = self.ids["product_table"]
        self.add_button = self.ids["add_button"]
        self.refresh_button = self.ids["refresh_button"]

        self.repo = ProductRepository(DatabaseManager())

        self.add_button.on_press = self.add_product
        self.refresh_button.on_press = self.refresh_products

        headers = [
            TableField("ID", .1, lambda p: _create_label(p.id)),
            TableField("Name", .2, lambda p: _create_label(p.name)),
            TableField("Target Stock", .2, lambda p: _create_label(p.target_stock)),
            TableField("Description", .3, lambda p: _create_desc_label(p.description)),
            TableField("Actions", .3, lambda p: _create_action_view(p, self.edit_product, self.remove_product))
        ]
        self.headers = headers

        self.products = self.repo.get_all_products()
        self.table.setup(self.headers, self.products)

    def refresh_products(self):
        self.products = self.repo.get_all_products()
        self.table.set_data(self.products)

    def add_product(self):
        def create_product(name, description, target_stock):
            prod = self.repo.create_product(name, description, target_stock)
            self.table.add_data_row(prod)

        popup = AddProductPopup(create_product)
        popup.open()

    def edit_product(self, product: ProductDalModel):
        def edit_product(name, description, target_stock):
            product.name = name
            product.description = description
            product.target_stock = target_stock
            new_prod = self.repo.edit_product(product)
            self.refresh_products()

        popup = EditProductPopup(product, edit_product)
        popup.open()

    def remove_product(self, product: ProductDalModel):
        self.products.remove(product)
        self.table.set_data(self.products)
        self.repo.delete_product(product.id)
        print("Remove product", product.id)
