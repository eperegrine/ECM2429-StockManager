from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from Data.DatabaseManager import DatabaseManager

Builder.load_file("Views/Screens/SettingsScreen.kv")


class SettingsScreen(Screen):
    db_manager: DatabaseManager

    def on_kv_post(self, base_widget):
        self.db_manager = DatabaseManager()

    def reset_database(self):
        self.db_manager.reset_database()

    def generate_data(self):
        print("Generating Data")
        self.db_manager.generate_test_data()
        print("Generated Data")
