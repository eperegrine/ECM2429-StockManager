from typing import Callable

from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang import Builder

from BackgroundColor import BackgroundColor

Builder.load_file("Views/Widgets/ActionsTableCell.kv")


class ActionsTableCell(BackgroundColor):
    edit_btn: Button
    remove_btn: Button
    obj: object

    def on_kv_post(self, base_widget):
        self.edit_btn = self.ids["edit_button"]
        self.remove_btn = self.ids["remove_button"]

    def setup(self, obj: object, edit: Callable, remove: Callable):
        self.obj = obj
        self.edit_btn.on_press = lambda: edit(obj)
        self.remove_btn.on_press = lambda: remove(obj)
