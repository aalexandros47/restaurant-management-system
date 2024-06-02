# Restaurant Management System

This Restaurant Management System allows users to manage menu items, reservations, orders, and payments in a restaurant setting. The system supports user roles for customers and staff, with functionalities such as viewing menus, making reservations, placing orders, and processing payments.

## Features

- **Menu Management**: View and update menu items.
- **Reservation System**: Make and manage table reservations.
- **Order System**: Place dine-in and takeaway orders.
- **Payment System**: Process payments via cash or card with validation.
- **User Authentication**: Login system for customers and staff.

## Prerequisites

- Python 3.x
- MySQL Server
- MySQL Workbench
- MySQL Connector for Python

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/restaurant-management-system.git
cd restaurant-management-system
```

### 2. Set Up the Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install mysql-connector-python
```

### 4. Configure MySQL Database

1. **Open MySQL Workbench** and connect to your MySQL server.
2. **Run the following SQL script** to create the database and tables:

```sql
CREATE DATABASE IF NOT EXISTS RestaurantDB;
USE RestaurantDB;

-- Drop existing tables in the correct order to avoid foreign key constraint errors
DROP TABLE IF EXISTS Payments;
DROP TABLE IF EXISTS Order_items;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Reservations;
DROP TABLE IF EXISTS Tables;
DROP TABLE IF EXISTS MenuItems;

-- Create tables
CREATE TABLE MenuItems (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    veg BOOLEAN NOT NULL,
    rating DECIMAL(3, 1) DEFAULT NULL,
    rating_count INT DEFAULT 0
);

INSERT INTO MenuItems (name, price, veg, rating, rating_count) VALUES
('Margherita Pizza', 8.99, TRUE, NULL, 0),
('Pepperoni Pizza', 9.99, FALSE, NULL, 0),
('Veggie Burger', 7.49, TRUE, NULL, 0),
('Cheeseburger', 8.49, FALSE, NULL, 0),
('Caesar Salad', 6.99, TRUE, NULL, 0),
('Chicken Salad', 7.99, FALSE, NULL, 0),
('Spaghetti Carbonara', 10.99, FALSE, NULL, 0),
('Penne Arrabbiata', 9.49, TRUE, NULL, 0),
('Mushroom Risotto', 11.49, TRUE, NULL, 0),
('Beef Lasagna', 12.49, FALSE, NULL, 0),
('Tomato Soup', 5.99, TRUE, NULL, 0),
('Chicken Noodle Soup', 6.49, FALSE, NULL, 0),
('Grilled Cheese Sandwich', 4.99, TRUE, NULL, 0),
('Ham and Cheese Sandwich', 5.49, FALSE, NULL, 0),
('Veggie Wrap', 6.49, TRUE, NULL, 0),
('Chicken Wrap', 6.99, FALSE, NULL, 0),
('Tacos', 7.99, FALSE, NULL, 0),
('Vegetable Stir Fry', 8.49, TRUE, NULL, 0),
('Grilled Salmon', 14.99, FALSE, NULL, 0),
('Cheese Omelette', 6.49, TRUE, NULL, 0);

CREATE TABLE Tables (
    table_id INT AUTO_INCREMENT PRIMARY KEY,
    capacity INT NULL,
    is_reserved BOOLEAN DEFAULT FALSE
);

CREATE TABLE Reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_id INT NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    reservation_time DATETIME NOT NULL,
    FOREIGN KEY (table_id) REFERENCES Tables(table_id)
);

CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    role ENUM('customer', 'staff') NOT NULL
);

CREATE TABLE Orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    table_id INT,
    total_price DECIMAL(10, 2),
    status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES Users(id),
    FOREIGN KEY (table_id) REFERENCES Tables(table_id)
);

CREATE TABLE Order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    menu_item_id INT,
    FOREIGN KEY (order_id) REFERENCES Orders(id),
    FOREIGN KEY (menu_item_id) REFERENCES MenuItems(id)
);

CREATE TABLE Payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_time DATETIME NOT NULL,
    payment_method VARCHAR(10) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(id)
);

INSERT INTO Tables (capacity) VALUES
(2),
(4),
(6),
(8),
(10);
```

### 5. Configure `db.py`

Update the `db.py` file with your MySQL credentials. Ensure the database name, username, and password are correct.

```python
import mysql.connector

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # Update with your MySQL root password
            database="RestaurantDB"
        )
        self.cursor = self.conn.cursor()
        self.reset_table_reservations()

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params or ())
        self.conn.commit()

    def fetch_all(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def fetch_one(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchone()

    def reset_table_reservations(self):
        self.execute_query("UPDATE tables SET is_reserved = FALSE")

db = Database()
```

### 6. Run the Application

```bash
python main.py
```

## Usage

### Customer Operations

1. **Login as Customer**: Enter your name to log in or create a new account.
2. **View Menu**: View the menu items available.
3. **Make Reservation**: Make a reservation by selecting a table and time.
4. **Place Order**: Place a dine-in or takeaway order and process the payment.
5. **Add Rating**: Add ratings to menu items.

### Staff Operations

1. **Login as Staff**: Enter your name to log in.
2. **Update Menu**: Add or delete menu items.
3. **View Sales**: View all sales records.

### Payment System

When placing an order, you will be prompted to choose a payment method (cash or card). The system validates the input and processes the payment accordingly.

## Troubleshooting

- **Database Connection Error**: Ensure that the MySQL server is running and the credentials in `db.py` are correct.
- **Table Not Found Error**: Ensure that the SQL script to create tables has been executed successfully.
- **Dependency Issues**: Ensure that all required Python packages are installed.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

### Contributors

This project was a collaborative effort by the following team members from Swinburne University of Technology, as part of the Software Engineering Architecture (SWE30003) unit:

- **Cong Quyen Pham**
  - GitHub: [Cong Quyen Pham](https://github.com/pcqisme)

- **Phuthai Hemathulintra**
  - GitHub: [Phuthai Hemathulintra](https://github.com/Phuthai2022)

- **Arnob Ghosh**
  - GitHub: [Arnob Ghosh](https://github.com/aalexandros47)

- **Lohan Thilakarathna**
  - GitHub: [Lohan Thilakarathna](https://github.com/lohanbt)



---

By following these instructions, you should be able to set up and run the Restaurant Management System successfully. If you encounter any issues or need further assistance, please feel free to contact us or open an issue on the GitHub repository.
