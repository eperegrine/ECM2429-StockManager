from typing import Tuple

import kivy.app
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget

kivy.app.Builder.load_file("Views/BackgroundColor.kv")


class BackgroundColor(Widget):
    background_color: Tuple[float, float, float, float]


class BackgroundLabel(BackgroundColor, Label):
    pass


class BackgroundButton(BackgroundColor, Button):
    pass


class BackgroundBoxLayout(BoxLayout, BackgroundColor):
    pass


class BackgroundStackLayout(StackLayout, BackgroundColor):
    pass
