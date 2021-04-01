from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

import class_manager
from Data.DatabaseManager import DatabaseManager
from Services import OrderFetchService, storefronts

Builder.load_file("Views/Screens/SettingsScreen.kv")


class SettingsScreen(Screen):
    db_manager: DatabaseManager

    def on_kv_post(self, base_widget):
        self.db_manager = class_manager.get_instance(DatabaseManager)

    def reset_database(self):
        self.db_manager.reset_database()

    def fetch_orders(self):
        def _completed(succeful, failed, orders):
            print("GOT ORDERS")
            print(succeful, failed, orders)

        service = class_manager.get_instance(OrderFetchService)
        service.fetch_orders(_completed)

    def generate_data(self):
        print("Generating Data")
        self.db_manager.generate_test_data()
        print("Generated Data")
