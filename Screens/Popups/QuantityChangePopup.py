import sys
from typing import Callable

from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from Data.Repositories.DalModels import ProductDalModel

Builder.load_file("Views/Screens/Popups/QuantityChangePopup.kv")


class QuantityChangePopup(Popup):
    label: Label
    qty_input: TextInput
    submit_btn: Button

    submit_callback: Callable[[int], None]

    min: int = 0
    max: int = sys.maxsize

    adding: bool = True

    quantity: int = 1

    def __init__(self, submit_callback: Callable[[int], None], adding=True, min=0, max=100, **kwargs):
        self.submit_callback = submit_callback
        self.min = min
        self.max = max
        self.adding = adding
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.size_hint_x = .4
        self.size_hint_y = .6
        self.label = self.ids['label']
        self.qty_input = self.ids['quantity_input']
        self.submit_btn = self.ids['submit_btn']

        self.submit_btn.on_press = self.on_submit
        self.qty_input.bind(text=self.on_qty_update)

    def on_qty_update(self, instance, value: str):
        if len(value) > 0:
            q = int(value)
            self.quantity = int(value)

        self.update_ui()

    def update_ui(self):
        valid = self.is_model_valid()
        self.submit_btn.disabled = not valid

    def is_model_valid(self):
        valid = self.min <= self.quantity <= self.max
        return valid

    def on_submit(self):
        if self.is_model_valid():
            self.submit_callback(self.quantity)
            self.dismiss()