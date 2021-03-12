import os
import sqlite3
from sqlite3 import Connection
from .Models import *

database_models = [ProductModel, StockItemModel, OrderModel, ProductOrderModel, ShipmentModel]


class DatabaseManager():
    """
    A class to manage the database connection
    handles initialising the database
    """
    _file_location = "stock_manager.db"

    def ensure_initialised(self):
        """
        Ensures that the database exists by initialising it if it doesn't
        """
        if not self.db_exists():
            self.initialise_database()

    def db_exists(self) -> bool:
        """
        Check if the database file exists

        :return: bool Whether or not the database exists
        """
        return os.path.exists(self._file_location)

    def reset_database(self):
        """
        Delete the database file
        """
        if self.db_exists():
            os.remove(self._file_location)

    def initialise_database(self):
        """
        Creates a database, overriding any existing database
        Sets up tables and relationships
        """
        self.reset_database()

        conn = self.get_connection()
        cur = conn.cursor()

        print("Creating tables...")

        for model in database_models:
            print("Creating Table %s" % model)
            model.create_table(cur)

        print ("Tables Created\n\nCreating Relations")

        # We setup the constraints afterwards to avoid issues
        # with constraints needing a table that is not yet created
        for model in database_models:
            print("Added contraint for %s" % model)
            model.add_constraints(cur)

        print("Created Tables")

        conn.commit()

    def generate_test_data(self):
        conn = self.get_connection()
        cur = conn.cursor()

        sql_file_name = os.path.join("SQLScripts", "SampleData.sql")
        sql_file = open(sql_file_name)
        sql_as_string = sql_file.read()
        cur.executescript(sql_as_string)

    def get_connection(self) -> Connection:
        """
        Creates a connection to the database

        :return: Connection A connection to the database
        """
        return sqlite3.connect(self._file_location)
