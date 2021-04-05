from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

import class_manager
from Data.DatabaseManager import DatabaseManager
from Services import PrintService

Builder.load_file("Views/Screens/SettingsScreen.kv")


class SettingsScreen(Screen):
    db_manager: DatabaseManager
    print_service: PrintService

    def on_kv_post(self, base_widget):
        self.db_manager = class_manager.get_instance(DatabaseManager)
        self.print_service = class_manager.get_instance(PrintService)

    def reset_database(self):
        self.db_manager.reset_database()

    def test_print(self):
        self.print_service.print("Hello, World!")

    def generate_data(self):
        print("Generating Data")
        self.db_manager.generate_test_data()
        print("Generated Data")
