from typing import Callable

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

Builder.load_file("Widgets/Table.kv")


class TableField:
    label: str = "Label"
    weight: float = .1
    _get_field_widget: Callable[[object], Widget]

    def __init__(self, label, weight, get_field):
        self.label = label
        self.weight = weight
        self._get_field_widget = get_field

    def create_label(self) -> Label:
        lbl = Label()
        lbl.text = self.label
        lbl.size_hint_x = self.weight
        return lbl

    def create_field(self, data) -> Widget:
        w = self._get_field_widget(data)
        w.size_hint_x = self.weight
        return w


class Table(Widget):

    table_header: BoxLayout
    table_body: BoxLayout
    scroll_view: ScrollView

    headers: [TableField]
    data: [object] = None

    def on_kv_post(self, base_widget):
        self.table_header = self.ids['table_header']
        self.table_body = self.ids['table_body']
        self.scroll_view = self.ids['scroll_view']

    def setup(self, headers: [TableField], data: [object]):
        self.headers = headers

        for header in headers:
            self.table_header.add_widget(header.create_label())

        self.set_data(data)

    def set_data(self, data: [object]):
        self.table_body.clear_widgets()
        row_height = .1
        height_hint = row_height * len(data)
        print(height_hint)
        self.table_body.size_hint_y = height_hint
        self.scroll_view.do_scroll_y = height_hint > 1

        for row in data:
            self.add_row(row)

        self.table_body.do_layout()
        self.scroll_view.update_from_scroll()
        self.data = data

    def add_row(self, row_data):
        row = BoxLayout()
        row.orientation = "horizontal"
        row.size_hint_y = .1
        for header in self.headers:
            row.add_widget(header.create_field(row_data))

        self.table_body.add_widget(row)