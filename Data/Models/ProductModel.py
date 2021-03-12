import sqlite3
from sqlite3 import Cursor


class ProductModel:
    id: int
    name: str
    description: str
    target_stock: int

    @staticmethod
    def create_table(cur: Cursor):
        cur.execute('''
        CREATE TABLE Products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            target_level INTEGER NOT NULL DEFAULT 1);
        ''')

    @staticmethod
    def add_constraints(cur: Cursor):
        """https://stackoverflow.com/a/23574053/3109126"""
        pass
