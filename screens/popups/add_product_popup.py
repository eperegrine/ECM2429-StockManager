from typing import Callable

from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from data.repositories.dal_models import ProductDalModel
from widgets import MinMaxIntInput

Builder.load_file("Views/screens/popups/AddProductPopup.kv")


class AddProductPopup(Popup):
    name_input: TextInput
    description_input: TextInput

    target_stock_input: MinMaxIntInput

    add_product_btn: Button
    add_product_callback: Callable[[str, str, int], None]

    target_stock: int = 0
    name: str = ""
    description: str = ""

    def __init__(self, add_product_callback: Callable[[str, str, int], None], **kwargs):
        super().__init__(**kwargs)
        self.add_product_callback = add_product_callback

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)

        self.size_hint_x = .6
        self.size_hint_y = .8

        self.add_product_btn = self.ids["add_product_btn"]
        self.add_product_btn.on_press = self.add_product
        self.name_input = self.ids["name_input"]
        self.name_input.bind(text=self.on_name_update)
        self.description_input = self.ids["description_input"]
        self.description_input.bind(text=self.on_description_update)

        self.target_stock_input = self.ids["target_stock_input"]
        self.target_stock_input.set_value(self.target_stock)
        self.target_stock_input.on_new_value = self.on_target_stock_update
        self.target_stock_input.min = 1

        self.update_add_btn()

    def on_name_update(self, _, value):
        self.name = value
        self.update_add_btn()

    def on_description_update(self, _, value):
        self.description = value
        self.update_add_btn()

    def on_target_stock_update(self, value: int):
        self.target_stock = value
        self.update_add_btn()

    def update_add_btn(self):
        self.add_product_btn.disabled = not self.is_model_valid()

    def is_model_valid(self):
        is_valid = len(self.name) > 0 and \
                   len(self.description) > 0 and \
                   self.target_stock is not None and \
                   0 <= self.target_stock
        return is_valid

    def add_product(self):
        if self.is_model_valid():
            values = (self.name, self.description, self.target_stock)
            self.add_product_callback(*values)
            self.dismiss()
        else:
            print("ERR: Add blocked due to invalid model")


class EditProductPopup(AddProductPopup):
    original_product: ProductDalModel = None

    def __init__(self, product: ProductDalModel, edit_product_callback: Callable[[str, str, int], None], **kwargs):
        self.original_product = product
        self.name = product.name
        self.description = product.description
        self.target_stock = product.target_stock
        super().__init__(edit_product_callback, **kwargs)

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.title = f"Edit Product #{self.original_product.id}"
        self.name_input.text = self.name
        self.description_input.text = self.description
        self.target_stock_input.set_value(self.target_stock)
        self.update_add_btn()
        # self.add_product_btn.text = "Edit Product"
