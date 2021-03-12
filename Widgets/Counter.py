from kivy.lang import Builder
from kivy.uix.widget import Widget

Builder.load_file("Widgets/Counter.kv")


class Counter(Widget):

    def on_kv_post(self, base_widget):
        self.update_counter()

    def increment(self):
        self.count += 1
        self.update_counter()

    def update_counter(self):
        count_lbl = self.ids['count_lbl']
        count_lbl.text = f"Counter: {self.count}"
