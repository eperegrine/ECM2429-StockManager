from sqlite3 import Cursor


class ProductOrderModel:
    id: int
    product_id: int
    price: int
    order_id: int
    """
    TODO: Use an enum
    1 - NotPicked
    2 - InProgress
    3 - Picked
    """
    picked_status: int

    @staticmethod
    def create_table(cur: Cursor):
        cur.execute('''
        CREATE TABLE ProductOrders (
            id INTEGER PRIMARY KEY,
            price INTEGER NOT NULL,
            picked_status INTEGER NOT NULL DEFAULT 1,
            quantity INTEGER NOT NULL DEFAULT 0);
        ''')

    @staticmethod
    def add_constraints(cur: Cursor):
        """https://stackoverflow.com/a/23574053/3109126"""
        cur.execute('''
        ALTER TABLE ProductOrders ADD COLUMN product_id INTEGER REFERENCES Products(id);
        ''')

        cur.execute('''
            ALTER TABLE ProductOrders ADD COLUMN order_id INTEGER REFERENCES Orders(id);
        ''')
