from typing import Callable, List

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget

import class_manager
from data.repositories import OrderRepository, StockRepository
from data.repositories.dal_models import OrderDalModel, ProductOrderDalModel, PickingStatus
from widgets import Table, TableField, create_label_cell

Builder.load_file("Views/Screens/Popups/StockPickerPopup.kv")


class StockPickerPopup(Popup):
    """
    A popup to handle picking stock

    Updates the data automatically, a done callback is called when closed
    """
    order_label: Label
    print_button: Button
    table: Table
    done_button: Button

    done_callback: Callable

    order: OrderDalModel = None
    order_repo: OrderRepository
    stock_repo: StockRepository

    headers: List[TableField]
    data: List[ProductOrderDalModel]

    def __init__(self, order: OrderDalModel, done_callback: Callable, **kwargs):
        self.order_repo = class_manager.get_instance(OrderRepository)
        self.stock_repo = class_manager.get_instance(StockRepository)
        self.order = order
        self.done_callback = done_callback
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.size_hint_x = .8
        self.size_hint_y = .9
        self.order_label = self.ids.order_label
        self.print_button = self.ids.print_button
        self.table = self.ids.table
        self.done_button = self.ids.done_button
        self.done_button.on_press = lambda: self.on_done()

        self.order_label.text = f"Order #{self.order.id:04d}"

        self.headers = [
            TableField("Item", .3, lambda po: create_label_cell(po.product.name)),
            TableField("Status", .2, lambda po: create_label_cell(po.status)),
            TableField("Locations", .2, lambda po: self._create_locations_cell(po)),
            TableField("Actions", .3, lambda po: self._create_actions_cell(po))
        ]

        self.data = self.order.products
        self.table.setup(self.headers, self.data)
        self.table.set_row_height(.3)

    def on_done(self):
        self.done_callback()
        self.dismiss()

    def _start_picking(self, po: ProductOrderDalModel):
        self.order_repo.start_picking(po)
        self.on_refresh()

    def _stop_picking(self, po: ProductOrderDalModel):
        self.order_repo.cancel_picking(po)
        self.on_refresh()

    def _mark_picked(self, po: ProductOrderDalModel):
        self.order_repo.pick_order_item(po)
        self.on_refresh()

    def _create_actions_cell(self, po: ProductOrderDalModel) -> Widget:
        if po.status == PickingStatus.NotPicked:
            stock = self.stock_repo.get_stock_for_product(po.product.id)
            if len(stock) > 0:
                btn = Button(text="Start Picking")
                btn.on_press = lambda: self._start_picking(po)
                return btn
            else:
                return create_label_cell("-")
        elif po.status == PickingStatus.InProgress:
            layout = BoxLayout(orientation="vertical")
            stop_btn = Button(text="Stop Picking")
            stop_btn.on_press = lambda: self._stop_picking(po)
            mark_picked_btn = Button(text="Mark as Picked")
            mark_picked_btn.on_press = lambda: self._mark_picked(po)
            layout.add_widget(stop_btn)
            layout.add_widget(mark_picked_btn)
            return layout
        else:
            return create_label_cell("-")

    def _create_locations_cell(self, po: ProductOrderDalModel) -> Label:
        if po.status == PickingStatus.Done:
            return create_label_cell("-")

        stock = self.stock_repo.get_stock_for_product(po.product.id)
        text = ""
        for si in stock:
            if len(text) != 0:
                text += "\n"
            text += f"{si.quantity} at {si.location}"
        if len(stock) == 0:
            text = "Out of Stock"
        return create_label_cell(text)

    def on_refresh(self):
        self.order = self.order_repo.get_order(self.order.id)
        self.data = self.order.products
        self.table.set_data(self.data)
