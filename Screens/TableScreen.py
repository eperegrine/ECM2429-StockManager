from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

from Widgets import Table, TableField


class TableScreen(Screen):
    """
    A Table Screen superclass to avoid repeating code for
    screens where the table is the main content
    """
    table: Table
    add_button: Button
    refresh_button: Button
    headers: [TableField]

    def __init__(self, headers: [TableField], **kw):
        self.headers = headers
        super().__init__(**kw)


    def on_kv_post(self, base_widget):
        self.table = self.ids["table"]
        self.add_button = self.ids["add_button"]
        self.refresh_button = self.ids["refresh_button"]

        self.add_button.on_press = self.on_add
        self.refresh_button.on_press = self.on_refresh

    def on_refresh(self):
        print("Refresh Not Implemented")

    def on_add(self):
        print("Add not implemented")