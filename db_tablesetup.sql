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
    payment_method VARCHAR(100) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(id)
);

INSERT INTO Tables (capacity) VALUES
(2),
(4),
(6),
(8),
(10);
