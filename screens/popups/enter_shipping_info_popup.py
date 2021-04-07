import sys
from typing import Callable

from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

Builder.load_file("Views/screens/popups/EnterShippingInfoPopup.kv")


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

        self.submit_btn.on_press = self._on_submit
        self.provider_input.bind(text=self._on_provider_update)
        self.tracking_code_input.bind(text=self._on_tracking_update)
        self._update_ui()

    def _on_provider_update(self, _, value: str):
        self.provider = value
        self._update_ui()

    def _on_tracking_update(self, _, value: str):
        self.tracking_code = value
        self._update_ui()

    def _update_ui(self):
        valid = self._is_model_valid()
        self.submit_btn.disabled = not valid

    def _is_model_valid(self):
        valid = len(self.provider) > 2 and len(self.tracking_code) > 5
        return valid

    def _on_submit(self):
        if self._is_model_valid():
            self.submit_callback(self.provider, self.tracking_code)
            self.dismiss()
