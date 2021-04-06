from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

import config
import screens

if config.DEV_MODE:
    import logging

    logger = logging.getLogger('peewee')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

Builder.load_file("main.kv")


class MainApp(Widget):
    screen_order = []
    screen_list = []
    nav_buttons = []

    sm: ScreenManager
    nav_bar: BoxLayout

    def set_screen(self, screen_name):
        """
        Sets the active screen and calculates an appropriate transition

        :param screen_name: The screen to transition to
        """
        current_screen = self.sm.current
        current_index = self.screen_order.index(current_screen)
        new_index = self.screen_order.index(screen_name)

        if current_index == new_index:
            return

        direction = "right" if current_index > new_index else "left"
        self.sm.transition.direction = direction
        self.sm.current = screen_name

    def on_kv_post(self, base_widget):
        """
        The method called by kivy after the widget has been created, used to initialise the UI
        """
        self.sm = self.ids["screen-manager"]
        self.nav_bar = self.ids["nav-bar"]

        self.add_screen(screens.HomeScreen(name="home"), nav_button_name="Home")
        self.add_screen(screens.OrdersScreen(name="orders"), nav_button_name="Orders")
        self.add_screen(screens.OrderDetailScreen(name="order_detail"))
        self.add_screen(screens.StockScreen(name="stock"), nav_button_name="Stock")
        self.add_screen(screens.ProductsScreen(name="products"), nav_button_name="Products")
        self.add_screen(screens.SettingsScreen(name="settings"), nav_button_name="Settings")

    def add_screen(self, screen: Screen, nav_button_name=None):
        """
        Add a Screen to the application and create relevant nav buttons

        :param screen: The screen to be added
        :param nav_button_name: The text for the nav button, when set to None will not add a nav button
        """
        self.screen_order.append(screen.name)
        self.screen_list.append(screen)
        self.sm.add_widget(screen)

        if nav_button_name is not None:
            nav_btn = Button()
            nav_btn.text = nav_button_name
            nav_btn.on_press = lambda: self.set_screen(screen.name)
            self.nav_buttons.append(nav_btn)
            self.nav_bar.add_widget(nav_btn)


class StockManagerApp(App):
    count = 0

    def build(self):
        self.title = "Stock Manager App"
        layout = MainApp()
        return layout


if __name__ == '__main__':
    StockManagerApp().run()
