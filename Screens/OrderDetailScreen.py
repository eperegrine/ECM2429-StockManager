from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from Data.Repositories.DalModels import OrderDalModel

Builder.load_file("Views/Screens/OrderDetailScreen.kv")


class OrderDetailScreen(Screen):
    order: OrderDalModel = None

    order_header_label: Label
    order_details_label: Label

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)

        self.order_header_label = self.ids.order_header_label
        self.order_details_label = self.ids.order_details_label

        self.update_ui()

    def set_order(self, o: OrderDalModel):
        print("SETTING DETAILS ORDER: ", o)
        self.order = o
        # self.update_ui()

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.update_ui()

    def update_ui(self):
        if self.order is not None:
            self.set_header_text()
            self.set_details_text()
        else:
            print("ORDER DETAILS SCREEN HAS NO ORDER")

    def set_details_text(self):
        self.order_details_label.text = f"""
[b][u]Customer[/u][/b]
[b]Name[/b]: {self.order.customer_name}
[b]Email[/b]: {self.order.email_address}
[b]Address[/b]: {self.order.address}"""

    def set_header_text(self):
        self.order_header_label.text = f"Order Details #{self.order.id:04d}"
