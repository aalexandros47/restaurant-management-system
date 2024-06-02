from table import Table
from db import db

class Reservation:
    def __init__(self, table, customer_name, reservation_time):
        self.db = db
        self.table = Table(table.table_id, table.capacity)
        self.customer_name = customer_name
        self.reservation_time = reservation_time

    def save(self):
        if self.table.is_available(self.reservation_time):
            query = "INSERT INTO Reservations (table_id, customer_name, reservation_time) VALUES (%s, %s, %s)"
            self.db.execute_query(query, (self.table.table_id, self.customer_name, self.reservation_time))
            print("Reservation saved successfully.")
        else:
            print("This table is not available at the selected time. Please choose another time or table.")
