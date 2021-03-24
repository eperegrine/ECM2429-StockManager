from typing import Callable

from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from Data.Repositories.DalModels import ProductDalModel

MAX_TARGET_STOCK = 100

Builder.load_file("Screens/Popups/AddProductPopup.kv")


class AddProductPopup(Popup):
    name_input: TextInput
    description_input: TextInput

    target_stock_lbl: Label
    increase_target_stock_btn: Button
    decrease_target_stock_btn: Button

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

        self.target_stock_lbl = self.ids["target_stock_lbl"]

        self.increase_target_stock_btn = self.ids["increase_target_stock_btn"]
        self.increase_target_stock_btn.on_press = self.increase_target_stock

        self.decrease_target_stock_btn = self.ids["decrease_target_stock_btn"]
        self.decrease_target_stock_btn.on_press = self.decrease_target_stock

        self.update_target_stock()

        self.update_add_btn()

    def on_name_update(self, instance, value):
        self.name = value
        self.update_add_btn()

    def on_description_update(self, instance, value):
        self.description = value
        self.update_add_btn()

    def decrease_target_stock(self):
        if self.target_stock > 0:
            self.target_stock = self.target_stock - 1
        self.update_target_stock()

    def increase_target_stock(self):
        if self.target_stock <= MAX_TARGET_STOCK - 1:
            self.target_stock = self.target_stock + 1
        self.update_target_stock()

    def update_target_stock(self):
        self.target_stock_lbl.text = f"Target Stock:\n{self.target_stock}"
        self.decrease_target_stock_btn.disabled = self.target_stock < 1
        self.increase_target_stock_btn.disabled = self.target_stock >= MAX_TARGET_STOCK
        self.update_add_btn()

    def update_add_btn(self):
        self.add_product_btn.disabled = not self.is_model_valid()

    def is_model_valid(self):
        is_valid = len(self.name) > 0 and \
                   len(self.description) > 0 and \
                   0 <= self.target_stock <= MAX_TARGET_STOCK
        return is_valid

    def add_product(self):
        if self.is_model_valid():
            values = (self.name, self.description, self.target_stock)
            print("Add Product", values)
            self.add_product_callback(*values)
            self.dismiss()
        else:
            print("ERR: Add blocked due to invalid model")


class EditProductPopup(AddProductPopup):
    original_product: ProductDalModel = None

    def __init__(self, product: ProductDalModel, edit_product_callback: Callable[[str, str, int], None], **kwargs):
        print("INIT", product)
        self.original_product = product
        self.name = product.name
        self.description = product.description
        self.target_stock = product.target_stock
        super().__init__(edit_product_callback, **kwargs)

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        print("kv_post")
        self.title = f"Edit Product #{self.original_product.id}"
        self.name_input.text = self.name
        self.description_input.text = self.description
        self.update_target_stock()
        self.update_add_btn()
        # self.add_product_btn.text = "Edit Product"
