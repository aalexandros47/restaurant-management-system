#table.py
import datetime
from db import *

class Table:
    def __init__(self, table_id, capacity):
        """
        Initialize a Table object with the given table_id and capacity.
        """
        self.table_id = table_id
        self.capacity = capacity

    def is_available(self, reservation_time):
        """
        Check if the table is available at the given reservation_time.
        """
        # Calculate the start and end times for the reservation window
        start_time = reservation_time - datetime.timedelta(hours=2)
        end_time = reservation_time + datetime.timedelta(hours=2)
        # Query to check if there are any reservations for the table within the reservation window
        query = """
        SELECT * FROM Reservations
        WHERE table_id = %s AND reservation_time BETWEEN %s AND %s
        """
        # Fetch the result of the query
        result = db.fetch_one(query, (self.table_id, start_time, end_time))
        # If result is None, the table is available; otherwise, it is not available
        return result is None
    
    @staticmethod
    def list_all_tables():
        """
        Retrieve a list of all tables from the database.
        """
        # Query to select all tables from the database
        query = "SELECT table_id, capacity FROM tables"
        rows = db.fetch_all(query)
        # Create a list of Table objects from the query result
        tables = [Table(table_id=row[0], capacity=row[1]) for row in rows]
        return tables
    
    @staticmethod
    def find_available_table(capacity):
        query = "SELECT table_id, capacity FROM tables WHERE capacity >= %s AND is_reserved = FALSE"
        tables = db.fetch_all(query, (capacity,))
        if tables:
            table_id = tables[0][0]
            db.execute_query("UPDATE tables SET is_reserved = TRUE WHERE table_id = %s", (table_id,))
            return table_id
        return None
