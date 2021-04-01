from typing import Callable

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from BackgroundColor import BackgroundBoxLayout, BackgroundColor, BackgroundLabel

Builder.load_file("Views/Widgets/Table.kv")


def create_label_cell(text) -> Widget:
    lbl = BackgroundLabel()
    lbl.halign = "center"
    lbl.valign = "center"
    lbl.text = str(text)
    # lbl.max_lines = 2
    return lbl


class TableField:
    label: str = "Label"
    weight: float
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

    def create_field(self, data, row_height) -> Widget:
        w = self._get_field_widget(data)
        w.size_hint_x = self.weight
        w.size_hint_max_y = row_height
        return w


even_row_colour_1 = (70 / 255, 70 / 255, 100 / 255, 1)
even_row_colour_2 = (75 / 255, 75 / 255, 100 / 255, 1)

odd_row_colour_1 = (50 / 255, 50 / 255, 100 / 255, 1)
odd_row_colour_2 = (55 / 255, 55 / 255, 100 / 255, 1)


class Table(Widget):
    table_header: BoxLayout
    table_body: BoxLayout
    scroll_view: ScrollView

    headers: [TableField]
    data: [object] = None

    row_height: float = .1

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

        for index, row in enumerate(data):
            self._add_row(row, index % 2 == 0)

        self.data = [*data]
        self.update_sizing()

    def set_row_height(self, height):
        self.row_height = height
        self.update_sizing()

    def update_sizing(self, old_size=None):
        height_hint = self.row_height * len(self.data)
        self.table_body.size_hint_y = height_hint
        self.scroll_view.do_scroll_y = height_hint > 1
        self.table_body.do_layout()
        self.scroll_view.update_from_scroll()

    def _add_row(self, row_data, even_row=False) -> Widget:
        row = BackgroundBoxLayout()
        row.orientation = "horizontal"
        row.size_hint_y = self.row_height

        row_col_1 = even_row_colour_1 if even_row else odd_row_colour_1
        row_col_2 = even_row_colour_2 if even_row else odd_row_colour_2

        row.background_color = row_col_1

        for index, header in enumerate(self.headers):
            field = header.create_field(row_data, self.row_height)
            if isinstance(field, BackgroundColor):
                if index % 2 == 1:
                    field.background_color = row_col_2
                else:
                    field.background_color = row_col_1
            row.add_widget(field)

        self.table_body.add_widget(row)
        return row

    def add_data_row(self, row_data):
        """
        Adds a data row with requiring the entire table to be rebuilt

        :param row_data: The row information
        """
        self._add_row(row_data, len(self.data) % 2 == 0)
        self.data.append(row_data)
        self.update_sizing()
