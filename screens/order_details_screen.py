from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

import class_manager
from data.repositories import StockRepository
from data.repositories.dal_models import OrderDalModel, OrderStatus, PickingStatus
from services import PrintService, MailService
from widgets.rich_text import bold, underline, size

Builder.load_file("Views/screens/OrderDetailScreen.kv")


class OrderDetailScreen(Screen):
    order: OrderDalModel = None

    order_header_label: Label
    order_details_label: Label
    # packing_list_label: Label

    stock_repo: StockRepository
    print_service: PrintService
    mail_service: MailService

    def __init__(self, **kw):
        super().__init__(**kw)
        self.stock_repo = class_manager.get_instance(StockRepository)
        self.print_service = class_manager.get_instance(PrintService)
        self.mail_service = class_manager.get_instance(MailService)

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)

        self.order_header_label = self.ids.order_header_label
        self.order_details_label = self.ids.order_details_label
        # self.packing_list_label = self.ids.packing_list_label

        self.update_ui()

    def set_order(self, o: OrderDalModel):
        print("SETTING DETAILS ORDER: ", o)
        self.order = o
        # self.update_ui()

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.update_ui()

    def print_address(self):
        self.print_service.print_order_address_label(self.order)

    def print_packing_list(self):
        self.print_service.print_order_packing_list(self.order)

    def open_mail_client(self):
        self.mail_service.open_blank_email(self.order.email_address)

    def update_ui(self):
        if self.order is not None:
            self.set_header_text()
            self.set_details_text()
            self.order_details_label.text_size = self.order_details_label.size
        else:
            print("ORDER DETAILS SCREEN HAS NO ORDER")

    def set_details_text(self):
        shipment_string = ""
        if self.order.shipment:
            shipment_string = f"""
{self.sub_title("Shipment")}
{bold("Provider")}: {self.order.shipment.provider}
{bold("Tracking Code")}: {self.order.shipment.tracking_code}"""
        else:
            shipment_string = f"{bold('Shipment')}: None"

        self.order_details_label.text = f"""{
self.sub_title("Details")}
{bold("Status")}: {self.order.status}
{bold("Storefront")}: {self.order.storefront}
{shipment_string}

{self.sub_title("Customer")}
{bold("Name")}: {self.order.customer_name}
{bold("Email")}: {self.order.email_address}
{bold("Address")}: {self.order.address}

{self.get_packing_list_text()}
"""

    def set_header_text(self):
        self.order_header_label.text = \
            size(f"Order Details {bold(f'#{self.order.id:04d}')}", 70)

    def get_packing_list_text(self) -> str:
        product_list_text: str = ""
        for po in self.order.products:
            stock = []
            status_msg = str(po.status)

            if self.order.status in [OrderStatus.Pending, OrderStatus.Picking] and\
                    po.status in [PickingStatus.NotPicked, PickingStatus.InProgress]:
                # if the order and the product have not been picked list the stock
                stock = self.stock_repo.get_stock_for_product(po.product.id)
                if len(stock) == 0:
                    status_msg += " - Out of Stock"

            product_list_text += f"{po.product.name}: {status_msg}\n"
            if len(stock) > 0:
                print("STOCK NOT EMPTY")
                for stock_item in stock:
                    product_list_text += (" " * 4) + f"- {stock_item.quantity:3} at {stock_item.location}\n"

        return f"""{
self.sub_title("Items")}
{product_list_text}
"""

    def sub_title(self, text):
        return size(bold(underline(text)), 50)
