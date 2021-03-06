from typing import Callable

from kivy.lang import Builder
from kivy.uix.widget import Widget

from screens.popups.add_product_popup import AddProductPopup, EditProductPopup
from screens.table_screen import TableScreen
from widgets import TableField, create_label_cell, ActionsTableCell
from data.repositories.dal_models import ProductDalModel
from data.repositories import ProductRepository

import class_manager

Builder.load_file("Views/Screens/ProductsScreen.kv")


def _create_desc_label(text) -> Widget:
    # TODO: Improve multiple line handling
    return create_label_cell(text)


def _create_action_view(product: ProductDalModel, edit: Callable, remove: Callable) -> Widget:
    action_cell = ActionsTableCell()
    action_cell.setup(product, edit, remove)
    return action_cell


class ProductsScreen(TableScreen):
    headers: [TableField]

    products: [ProductDalModel]

    repo: ProductRepository

    def __init__(self, **kw):
        # self.repo = ProductRepository(DatabaseManager())
        self.repo = class_manager.get_instance(ProductRepository)
        self.products = self.repo.get_all_products()
        headers = [
            TableField("ID", .1, lambda p: create_label_cell(p.id)),
            TableField("Name", .2, lambda p: create_label_cell(p.name)),
            TableField("Target Stock", .2, lambda p: create_label_cell(p.target_stock)),
            TableField("Description", .3, lambda p: _create_desc_label(p.description)),
            TableField("Actions", .3, lambda p: _create_action_view(p, self.edit_product, self.remove_product))
        ]
        super().__init__(headers, **kw)

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.table.setup(self.headers, self.products)
        self.table.set_row_height(.2)

    def on_refresh(self):
        self.products = self.repo.get_all_products()
        self.table.set_data(self.products)

    def on_add(self):
        def create_product(name, description, target_stock):
            prod = self.repo.create_product(name, description, target_stock)
            self.products.append(prod)
            self.table.set_data(self.products)
            # BUG: Row is added at incorrect size and not removed properly
            # Therefore not using a more efficient method to add row
            # self.table.add_data_row(prod)

        popup = AddProductPopup(create_product)
        popup.open()

    def edit_product(self, product: ProductDalModel):
        def edit_product(name, description, target_stock):
            product.name = name
            product.description = description
            product.target_stock = target_stock
            new_prod = self.repo.edit_product(product)
            self.on_refresh()

        popup = EditProductPopup(product, edit_product)
        popup.open()

    def remove_product(self, product: ProductDalModel):
        self.products = list(filter(lambda p: not p.id == product.id, self.products))
        self.repo.delete_product(product.id)
        self.table.set_data(self.products)
