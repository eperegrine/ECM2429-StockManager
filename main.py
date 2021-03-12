from kivy.app import App, Builder
from kivy.uix.widget import Widget

Builder.load_file("main.kv")


class MainApp(Widget):
    pass


class StockManagerApp(App):
    count = 0

    def build(self):
        layout = MainApp()
        return layout


if __name__ == '__main__':
    StockManagerApp().run()
