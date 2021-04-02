import sys
from typing import Callable

from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

Builder.load_file("Views/Screens/Popups/EnterShippingInfoPopup.kv")


class EnterShippingInfoPopup(Popup):
    provider_input: TextInput
    tracking_code_input: TextInput
    submit_btn: Button

    submit_callback: Callable[[str, str], None]

    provider: str = ""
    tracking_code: str = ""

    def __init__(self, submit_callback: Callable[[str, str], None], **kwargs):
        self.submit_callback = submit_callback
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.size_hint_x = .4
        self.size_hint_y = .6
        self.provider_input = self.ids.provider_input
        self.tracking_code_input = self.ids.tracking_code_input
        self.submit_btn = self.ids['submit_btn']

        self.submit_btn.on_press = self.on_submit
        self.provider_input.bind(text=self.on_provider_update)
        self.tracking_code_input.bind(text=self.on_tracking_update)
        self.update_ui()

    def on_provider_update(self, _, value: str):
        self.provider = value
        self.update_ui()

    def on_tracking_update(self, _, value: str):
        self.tracking_code = value
        self.update_ui()

    def update_ui(self):
        valid = self.is_model_valid()
        self.submit_btn.disabled = not valid

    def is_model_valid(self):
        valid = len(self.provider) > 2 and len(self.tracking_code) > 5
        return valid

    def on_submit(self):
        if self.is_model_valid():
            self.submit_callback(self.provider, self.tracking_code)
            self.dismiss()
