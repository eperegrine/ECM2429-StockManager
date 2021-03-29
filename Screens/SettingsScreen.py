from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from Data.DatabaseManager import DatabaseManager

Builder.load_file("Screens/SettingsScreen.kv")


class SettingsScreen(Screen):
    db_manager: DatabaseManager

    def on_kv_post(self, base_widget):
        self.db_manager = DatabaseManager()

    def create_database(self):
        print("Creating Database")
        self.db_manager.initialise_database()
        print("Created Database")

    def generate_data(self):
        print("Generating Data")
        self.db_manager.generate_test_data()
        print("Generating Data")
