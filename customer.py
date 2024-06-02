from user import User
from reservation import Reservation
import datetime
from OrderFactory import OrderFactory
from table import Table
from restaurant import RestaurantSystem
from menu import Menu

restaurant = RestaurantSystem()
menu = Menu()

class Customer(User):

    def make_reservation(self):
        """
        Make a reservation by selecting a table and saving the reservation to the database.
        """
        print("Making a reservation:")
        while True:
            try:
                reservation_time_input = input("Enter reservation time (YYYY-MM-DD HH:MM:SS): ").strip()
                reservation_time = datetime.datetime.strptime(reservation_time_input, "%Y-%m-%d %H:%M:%S")
                break
            except ValueError:
                print("Invalid date-time format. Please enter the reservation time in the format YYYY-MM-DD HH:MM:SS.")
                continue
        
        # Get a list of available tables for the given reservation time
        available_tables = self.available_tables(reservation_time)
        
        if not available_tables:
            print("No tables available at this time. Please choose another time.")
            return

        print("Available Tables:")
        for table in available_tables:
            print(f"Table ID: {table.table_id}, Capacity: {table.capacity}")

        while True:
            try:
                table_id = int(input("Choose a table by ID: ").strip())
                if any(table.table_id == table_id for table in available_tables):
                    break
                else:
                    print("Table ID not found in the available tables. Please enter a valid table ID.")
                break
            except ValueError:
                print("Invalid input. Please enter a valid table ID.")
                continue

        for table in available_tables:
            if table.table_id == table_id:
                reservation = Reservation(table, self.name, reservation_time)
                reservation.save()
                break


    def available_tables(self, reservation_time):
        """
        Get a list of available tables for the given reservation time.

        """
        from table import Table
        all_tables = Table.list_all_tables()  # Get all tables from the database
        return [table for table in all_tables if table.is_available(reservation_time)]


    def add_rating(self, menu):
        print(f"{self.name}, you can add a rating to the menu items:")
        menu.show_menu()
        while True:
            try:
                item_id = int(input('Enter item ID to rate: '))
                if not any(item.id == item_id for item in menu.items):
                    print("Invalid item ID. Please enter a valid item ID.")
                    continue
                rating = int(input('Enter rating (1-5): '))
                if rating not in range(1, 6):
                    print('Invalid rating. Please enter a number between 1 and 5.')
                    continue
                menu.add_rating(item_id, rating)
                break
            except ValueError:
                print("Invalid input. Please enter a numeric value for both item ID and rating.")

    def place_dine_in_order(self, customer_id):
        while True:
            try:
                num_people = int(input("Enter the number of people: ").strip())
                if num_people <= 0:
                    raise ValueError("Number of people must be greater than 0.")
                break
            except ValueError as e:
                print(f"Error: {e}. Please enter a valid number of people.")        
        table_id = Table.find_available_table(num_people)
        if table_id:
            while True:
                item_ids_input = input("Enter the item IDs to order (comma-separated): ").strip()
                if not item_ids_input:
                    print("Item IDs cannot be empty. Please try again.")
                    continue
                try:
                    item_ids = [int(item_id.strip()) for item_id in item_ids_input.split(",")]
                    if any(not menu.item_exists(item_id) for item_id in item_ids):
                        raise ValueError("One or more item IDs do not exist in the menu.")
                    break
                except ValueError as e:
                    print(f"Error: {e}. Please enter valid item IDs.")
            order_id = OrderFactory.create_order("DineIn", customer_id, item_ids, table_id)
            restaurant.kitchen.notify(order_id)
        else:
            print("No available tables for the specified number of people.")

    def place_takeaway_order(self, customer_id):
        while True:
            item_ids_input = input("Enter the item IDs to order (comma-separated): ").strip()
            if not item_ids_input:
                print("Item IDs cannot be empty. Please try again.")
                continue        
            try:
                item_ids = [int(item_id.strip()) for item_id in item_ids_input.split(",")]
                if any(not menu.item_exists(item_id) for item_id in item_ids):
                    raise ValueError("One or more item IDs do not exist in the menu.")
                break
            except ValueError as e:
                print(f"Error: {e}. Please enter valid item IDs.")
        order_id = OrderFactory.create_order("TakeAway", customer_id, item_ids)
        restaurant.kitchen.notify(order_id)
