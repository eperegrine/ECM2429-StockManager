from typing import Callable

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

from Widgets import Table, TableField

Builder.load_file("Screens/ProductsScreen.kv")

from Data.Repositories.DalModels import ProductDalModel


def _create_label(text) -> Widget:
    lbl = Label()
    lbl.text = str(text)
    return lbl


def _create_action_view(product: ProductDalModel, edit: Callable, remove: Callable) -> Widget:
    # TODO: add view class
    layout = BoxLayout()
    layout.orientation = "horizontal"

    edit_btn = Button()
    edit_btn.text = "Edit"
    edit_btn.on_press = lambda: edit(product)
    remove_btn = Button()
    remove_btn.text = "Remove"
    remove_btn.on_press = lambda: remove(product)

    layout.add_widget(edit_btn)
    layout.add_widget(remove_btn)
    return layout


class ProductsScreen(Screen):
    table: Table
    add_button: Button

    products: [ProductDalModel]

    def on_kv_post(self, base_widget):
        self.table = self.ids["product_table"]
        self.add_button = self.ids["add_button"]

        self.add_button.on_press = self.add_product

        headers = [
            TableField("ID", .1, lambda p: _create_label(p.id)),
            TableField("Name", .2, lambda p: _create_label(p.name)),
            TableField("Target Stock", .2, lambda p: _create_label(p.target_stock)),
            TableField("Description", .3, lambda p: _create_label(p.description)),
            TableField("Actions", .3, lambda p: _create_action_view(p, self.edit_product, self.remove_product))
        ]

        products: [ProductDalModel] = []

        for i in range(5):
            products.append(ProductDalModel(i, f"iPhone {i}", "Apple iPhone X", 10))

        self.products = products

        self.table.setup(headers, products)

    def add_product(self):
        i = len(self.products)
        product = ProductDalModel(i, f"iPhone {i}", "Apple iPhone X", 10)
        self.products.append(product)

        self.table.set_data(self.products)

    def edit_product(self, product: ProductDalModel):
        print("Edit product", product.id)

    def remove_product(self, product: ProductDalModel):
        self.products.remove(product)
        self.table.set_data(self.products)
        print("Remove product", product.id)
