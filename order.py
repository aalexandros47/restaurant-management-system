from db import db

class Order:
    def __init__(self, id, customer_id, items, total_price, status='Pending'):
        self.id = id
        self.customer_id = customer_id
        self.items = items
        self.total_price = total_price
        self.status = status

    @staticmethod
    def place_order(customer_id, item_ids):
        items = [db.fetch_one("SELECT id, price FROM menuitems WHERE id = %s", (item_id,)) for item_id in item_ids]
        total_price = sum(item[1] for item in items)
        db.execute_query("INSERT INTO orders (customer_id, total_price, status) VALUES (%s, %s, %s)",
                         (customer_id, total_price, 'Pending'))
        order_id = db.cursor.lastrowid
        for item in items:
            db.execute_query("INSERT INTO order_items (order_id, menu_item_id) VALUES (%s, %s)", (order_id, item[0]))
        print(f"Order placed for customer {customer_id}.")
        return order_id

