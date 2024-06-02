from db import *
from staff import Staff
from menu import Menu
from kitchen import Kitchen
from OrderFactory import OrderFactory
from payment_strategy import PaymentStrategy

class RestaurantSystem:
    def __init__(self):
        self.kitchen = Kitchen()
        self.menu = Menu()

    def handle_customer(self, name):
        while True:
            user = db.fetch_one("SELECT id, username FROM users WHERE username = %s AND role = 'customer'", (name,))
            if user:
                print(f"Welcome back, {user[1]}!")
                return user[0]  # Return customer_id
            else:
                print("New customer detected. Please provide additional information.")
                while True:
                    password = input("Enter a password: ").strip()
                    if not password:
                        print("Password cannot be empty. Please try again.")
                        continue
                    else:
                        db.execute_query("INSERT INTO users (username, password, role) VALUES (%s, %s, 'customer')", (name, password))
                        user_id = db.cursor.lastrowid
                        print(f"Welcome, {name}! Your information has been inserted into the database successfully.")
                        return user_id  # Return user_id


    def handle_staff(self, username):
        while True:
            user = db.fetch_one("SELECT id, username FROM users WHERE username = %s AND role = 'staff'", (username,))
            if user:
                print(f"Welcome back, {user[1]}!")
                return Staff(user[1])  # Return an instance of the Staff class
            else:
                print("New staff detected. Please provide additional information.")
                while True:
                    password = input("Enter a password: ").strip()
                    if not password:
                        print("Password cannot be empty. Please try again.")
                        continue
                    else:
                        db.execute_query("INSERT INTO users (username, password, role) VALUES (%s, %s, 'staff')", (username, password))
                        user_id = db.cursor.lastrowid
                        print(f"Welcome, {username}! Your information has been inserted into the database successfully.")
                        return Staff(username)  # Return an instance of the Staff class

    def show_all_sales(self):
        query = """
        SELECT o.id, u.username, o.table_id, o.total_price, p.payment_time
        FROM orders o
        JOIN users u ON o.customer_id = u.id
        JOIN payments p ON o.id = p.order_id
        WHERE o.status = 'Paid'
        """
        orders = db.fetch_all(query)
        if orders:
            print("\nAll Sales:")
            for order in orders:
                table_info = f", Table ID: {order[2]}" if order[2] else ""
                print(f"Order ID: {order[0]}, Customer: {order[1]}{table_info}, Total Price: ${order[3]}, Payment Time: {order[4]}")
        else:
            print("No sales found.")

    def process_payment(self, customer_id):
        orders = db.fetch_all("SELECT id, total_price FROM orders WHERE customer_id = %s AND status = 'Pending'", (customer_id,))
        if orders:
            print("Orders:")
            for order in orders:
                print(f"{order[0]}. Total: ${order[1]}")

            while True:
                try:
                    order_id = int(input("Enter the order ID to pay: ").strip())
                    if any(order[0] == order_id for order in orders):
                        break
                    else:
                        print("Invalid order ID. Please enter a valid order ID from the list above.")
                except ValueError:
                    print("Invalid input. Please enter a numeric value for the order ID.")
            
            amount = db.fetch_one("SELECT total_price FROM orders WHERE id = %s", (order_id,))[0]
            print(f"The total amount to be paid is ${amount}.")

            valid_payment_methods = ["Card", "Cash", "DWallet"]
            while True:
                payment_method = input("Enter the payment method (Card [Credit Card]/Cash/DWallet[Digital Wallet]): ").strip()
                if payment_method in valid_payment_methods:
                    break
                else:
                    print(f"Invalid payment method. Please choose from {valid_payment_methods}.")

            try:
                db.execute_query("INSERT INTO payments (order_id, payment_method, amount, payment_time) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)",
                                (order_id, payment_method[:50], amount))  # Truncate payment method if necessary
            except mysql.connector.errors.DataError as e:
                if "Data too long" in str(e):
                    print("Payment method is too long. Truncating to fit the column's maximum length.")
                    truncated_payment_method = payment_method[:50]  # Truncate to fit column's maximum length
                    db.execute_query("INSERT INTO payments (order_id, payment_method, amount, payment_time) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)",
                                    (order_id, truncated_payment_method, amount))
                else:
                    raise  # Reraise the exception if it's not related to data length

            print("Payment processed successfully.")
        else:
            print("No pending orders found.")
