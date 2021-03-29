import sys
from typing import Callable

from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from Data import DatabaseManager
from Data.Repositories import ProductRepository
from Data.Repositories.DalModels import ProductDalModel, StockItemDalModel
from Widgets import MinMaxIntInput

Builder.load_file("Screens/Popups/StockItemEditorPopup.kv")


class StockItemEditorPopup(Popup):
    product_spinner: Spinner
    location_input: TextInput
    quantity_input: MinMaxIntInput
    save_btn: Button

    save_callback: Callable[[int, str, int], None]

    product: ProductDalModel = None
    location: str = ""
    quantity: int = None

    def __init__(self, save_callback: Callable[[int, str, int], None], **kwargs):
        self.product_repo = ProductRepository(DatabaseManager())
        self.save_callback = save_callback
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.size_hint_x = .6
        self.size_hint_y = .8

        self.product_spinner = self.ids['product_spinner']
        self.location_input = self.ids['location_input']
        self.quantity_input = self.ids['quantity_input']
        self.save_btn = self.ids['save_btn']

        self.setup_dropdown()
        self.quantity_input.on_new_value = self.on_quantity
        self.location_input.bind(text=self.on_location)
        self.save_btn.on_press = self.on_save

        self.quantity_input.set_value(0 if self.quantity is None else self.quantity)
        self.location_input.text = self.location

        self.update_ui()

    def setup_dropdown(self):
        prods = self.product_repo.get_all_products()
        self.product_spinner.values = [p.name for p in prods]

        def _select(_, name):
            products_with_name = [p for p in prods if p.name == name]
            product = products_with_name[0]
            self.select_product(product)

        if self.product is not None:
            self.product_spinner.text = self.product.name

        self.product_spinner.bind(text=_select)

    def select_product(self, product: ProductDalModel):
        self.product = product
        print("Selected Product:", product.id, product.name, product.target_stock)
        self.update_ui()

    def on_quantity(self, value: int):
        self.quantity = value
        self.update_ui()

    def on_location(self, _, value: str):
        self.location = value
        self.update_ui()

    def is_model_valid(self):
        return self.product is not None and \
               len(self.location) > 0 and \
               self.quantity is not None and \
               self.quantity > 0

    def update_ui(self):
        self.save_btn.disabled = not self.is_model_valid()

    def on_save(self):
        if self.is_model_valid():
            print("Success")
            self.save_callback(self.product.id, self.location, self.quantity)
            self.dismiss()
        else:
            print("Model invalid")


class EditStockItemPopup(StockItemEditorPopup):
    def __init__(self, stock_item: StockItemDalModel, save_callback: Callable[[int, str, int], None], **kwargs):
        self.quantity = stock_item.quantity
        self.location = stock_item.location
        self.product = stock_item.product
        super().__init__(save_callback, **kwargs)

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.title = "Edit Stock Item"
        self.product_spinner.disabled = True


class AddStockItemPopup(StockItemEditorPopup):
    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.title = "Add Stock Item"
