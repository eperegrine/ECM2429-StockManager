import re

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


# TODO: implement min max
# if substring.isdigit():
#     num = int(substring)
# else:
#     digits = [c for c in substring if c.isdigit()]
#     num = int("".join(digits)) if len(digits) > 0 else 0
#
# if self.min is not None and num < self.min:
#     num = self.min
# elif self.max is not None and num > self.max:
#     num = self.max

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
    max: int

    def __init__(self, min=None, max=None, **kwargs):
        self.min = min
        self.max = max
        super().__init__(**kwargs)

    def insert_text(self, substring: str, from_undo=False):
        super().insert_text(substring, from_undo)
        self.validate()

    def validate(self):
        num = int(self.text)

        if self.min is not None and num < self.min:
            num = self.min
        elif self.max is not None and num > self.max:
            num = self.max

        print("validating", num)
        self.text = str(num)

