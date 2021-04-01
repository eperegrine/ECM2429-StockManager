from typing import Callable

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

import class_manager
from BackgroundColor import BackgroundColor
from Data.Repositories.DalModels import OrderDalModel, OrderStatus
from Data.Repositories.OrderRepository import OrderRepository
from Screens.TableScreen import TableScreen
from Services import OrderSyncService
from Widgets import TableField, create_label_cell

Builder.load_file("Views/Screens/OrdersScreen.kv")


def _create_products_cell(o: OrderDalModel) -> Label:
    prod_names = [p.product.name for p in o.products]
    return create_label_cell("\n".join(prod_names))


def _create_action_cell(o: OrderDalModel, view: Callable, pick_stock: Callable, ship: Callable, close: Callable):
    cell = OrdersActionTableCell(o, view, pick_stock, ship, close)
    return cell


class OrdersActionTableCell(BackgroundColor):
    layout: BoxLayout

    view_button: Button
    pick_stock_button: Button
    ship_button: Button
    close_button: Button
    order: OrderDalModel

    view: Callable[[OrderDalModel], None]
    pick_stock: Callable[[OrderDalModel], None]
    ship: Callable[[OrderDalModel], None]
    close: Callable[[OrderDalModel], None]

    def __init__(self, order: OrderDalModel, view: Callable, pick_stock: Callable, ship: Callable, close: Callable,
                 **kwargs):
        self.order = order
        self.view = lambda: view(order)
        self.pick_stock = lambda: pick_stock(order)
        self.ship = lambda: ship(order)
        self.close = lambda: close(order)
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        self.layout = self.ids.layout
        self.view_button = self.ids.view_button
        self.pick_stock_button = self.ids.pick_stock_button
        self.ship_button = self.ids.ship_button
        self.close_button = self.ids.close_button

        self.view_button.on_press = self.view
        self.pick_stock_button.on_press = self.pick_stock
        self.ship_button.on_press = self.ship
        self.close_button.on_press = self.close
        self.update_ui()

    def update_ui(self):
        status = self.order.status
        self._hide_or_show(self.pick_stock_button, status in [OrderStatus.Picking, OrderStatus.Pending])
        self._hide_or_show(self.ship_button, status == OrderStatus.Picking)
        self._hide_or_show(self.close_button, status == OrderStatus.Shipped)
        self.layout.do_layout()

    def _hide_or_show(self, button: Button, show_condition: bool):
        if show_condition:
            self._show(button)
        else:
            self._hide(button)

    def _hide(self, w: Button):
        self.layout.remove_widget(w)

    def _show(self, b: Button):
        if b not in self.layout.children:
            self.add_widget(b)


class OrdersScreen(TableScreen):
    orders: [OrderDalModel]
    sync_service: OrderSyncService

    sync_button: Button

    def __init__(self, **kw):
        self.repo = class_manager.get_instance(OrderRepository)
        self.sync_service = class_manager.get_instance(OrderSyncService)
        self.orders = self.repo.get_all_orders()
        headers = [
            TableField("ID", .1, lambda o: create_label_cell(o.id)),
            TableField("Customer", .25, lambda o: create_label_cell(o.customer_name + "\n" + o.email_address)),
            TableField("Status", .1, lambda o: create_label_cell(o.status)),
            TableField("Store", .1, lambda o: create_label_cell(o.storefront)),
            TableField("Products", .15, lambda o: _create_products_cell(o)),
            TableField("Actions", .2, lambda o: self.create_action_cell(o))
        ]
        super().__init__(headers, **kw)
        self.sync_button = self.ids.sync_button
        self.sync_button.on_press = self.on_sync
        self.table.set_row_height(.25)

    def create_action_cell(self, o):
        return _create_action_cell(o, self.view_order, self.pick_stock, self.ship_order, self.close_order)

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.table.setup(self.headers, self.orders)

    def on_refresh(self):
        self.orders = self.repo.get_all_orders()
        self.table.set_data(self.orders)

    def on_sync(self):
        self.sync_service.sync(lambda: self.on_refresh())

    def view_order(self, o: OrderDalModel):
        pass

    def pick_stock(self, o: OrderDalModel):
        pass

    def ship_order(self, o: OrderDalModel):
        pass

    def close_order(self, o: OrderDalModel):
        pass
