from sqlite3 import Cursor


class OrderModel:
    id: int
    customer_name: str
    """
    TODO: use Enum
    1 - Pending
    2 - Picking
    3 - Shipped
    4 - Closed
    """
    status: int
    target_stock: int
    closed: bool

    @staticmethod
    def create_table(cur: Cursor):
        cur.execute('''
            CREATE TABLE Orders (
                id INTEGER PRIMARY KEY,
                customer_name TEXT,
                status INTEGER NOT NULL DEFAULT 1,
                target_stock INTEGER NOT NULL DEFAULT 2,
                quantity INTEGER NOT NULL DEFAULT 0,
                closed BOOLEAN NOT NULL DEFAULT false);
            ''')

    @staticmethod
    def add_constraints(cur: Cursor):
        pass