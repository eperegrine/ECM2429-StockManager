from sqlite3 import Cursor


class StockItemModel():
    id: int
    product_id: int
    location: str
    quantity: int

    @staticmethod
    def create_table(cur: Cursor):
        cur.execute('''
        CREATE TABLE StockItems (
            id INTEGER PRIMARY KEY,
            location TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0);
        ''')

    @staticmethod
    def add_constraints(cur: Cursor):
        """https://stackoverflow.com/a/23574053/3109126"""
        cur.execute('''
        ALTER TABLE StockItems ADD COLUMN product_id INTEGER REFERENCES Products(id);
        ''')