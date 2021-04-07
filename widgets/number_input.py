import re
from typing import Callable

from kivy.uix.textinput import TextInput


class FloatInput(TextInput):
    """
    Sourced from: https://kivy.org/doc/stable/api-kivy.uix.textinput.html
    """
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)


class IntInput(TextInput):
    """
    A input field that is limited to only numbers
    """

    def insert_text(self, substring: str, from_undo=False):
        s = ""
        # Allow negative numbers by allowing a dash at the start
        if substring.isdigit() or \
                self.cursor_col == 0 and substring[0] == "-":
            s = substring
        return super(IntInput, self).insert_text(s, from_undo=from_undo)


class MinMaxIntInput(IntInput):
    """
    A input filed that is limited to only numbers
    """

    min: int
    # sql int max
    max: int = 2147483647

    on_new_value: Callable[[int], None]

    def __init__(self, min=None, max=2147483647, **kwargs):
        self.min = min
        self.max = max
        self.on_new_value = lambda n: n
        super().__init__(**kwargs)

    def _set_line_text(self, line_num, text):
        super()._set_line_text(line_num, text)
        self.validate()

    def paste(self):
        super().paste()
        self.validate()

    def set_value(self, value: int):
        self.text = str(value)
        self.validate()

    def validate(self):
        if len(self.text) == 0:
            self.on_new_value(None)
            return
        num = int(self.text)

        if self.min is not None and num < self.min:
            num = self.min
        elif self.max is not None and num > self.max:
            num = self.max

        self.on_new_value(num)
        self.text = str(num)
