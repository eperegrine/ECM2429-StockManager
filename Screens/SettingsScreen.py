from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from Data.DatabaseManager import DatabaseManager
from Services import OrderSyncService, storefronts

Builder.load_file("Views/Screens/SettingsScreen.kv")


class SettingsScreen(Screen):
    db_manager: DatabaseManager

    def on_kv_post(self, base_widget):
        self.db_manager = DatabaseManager()

    def reset_database(self):
        self.db_manager.reset_database()

    def fetch_orders(self):
        def _completed(succeful, failed, orders):
            print("GOT ORDERS")
            print(succeful, failed, orders)

        service = OrderSyncService(storefronts)
        service.sync_orders(_completed)

    def generate_data(self):
        print("Generating Data")
        self.db_manager.generate_test_data()
        print("Generated Data")
