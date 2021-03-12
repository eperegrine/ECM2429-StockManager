from sqlite3 import Cursor


class ShipmentModel():
    id: int
    order_id: int
    provider: str
    tracking_code: str

    @staticmethod
    def create_table(cur: Cursor):
        cur.execute('''
        CREATE TABLE Shipments (
            id INTEGER PRIMARY KEY,
            provider TEXT NOT NULL,
            tracking_code TEXT NOT NULL);
        ''')

    @staticmethod
    def add_constraints(cur: Cursor):
        """https://stackoverflow.com/a/23574053/3109126"""
        cur.execute('''
        ALTER TABLE Shipments ADD COLUMN order_id INTEGER REFERENCES Orders(id);
        ''')