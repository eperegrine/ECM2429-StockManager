from data import DatabaseManager


class Repository:
    """
    Act as a buffer between the data layer and the application layer
    """
    db_manager: DatabaseManager

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.db_manager.ensure_initialised()
