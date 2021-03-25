import os
from .Models import *

import config

class DatabaseManager():
    """
    A class to manage the database connection
    handles initialising the database
    """
    _file_location = str(config.database_store)

    def ensure_initialised(self):
        """
        Ensures that the database exists by initialising it if it doesn't
        """
        print ("Managing database at " + self._file_location)
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
        Delete the database file if it exists
        """
        if self.db_exists():
            os.remove(self._file_location)

    def initialise_database(self):
        """
        Creates a database, overriding any existing database
        Sets up tables and relationships
        """
        self.reset_database()

        db.connect()

        db.create_tables(model_list)

    def generate_test_data(self):
        """
        Generates data useful for testing

        :return: None
        """
        iphone_x = Product(name="iPhone X", description="Apple iPhone\nwith FaceID", target_stock=3)
        air_pods = Product(name="AirPods", description="Apple Wireless EarBuds", target_stock=10)
        i_pad = Product(name="iPad", description="Apple tablet", target_stock = 5)

        for product in [iphone_x, air_pods, i_pad]:
            product.save()

        stock = [
            StockItem(product=iphone_x, location="A12", quantity=3),
            StockItem(product=iphone_x, location="B3", quantity=1),
            StockItem(product=air_pods, location="A4", quantity=10),
            StockItem(product=i_pad, location="C2", quantity=3)
        ]

        for s in stock:
            s.save()
