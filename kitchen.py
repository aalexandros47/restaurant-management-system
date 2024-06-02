from db import *

class Kitchen:
    def __init__(self):
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)
        print(f"Order {order['id']} for customer {order['customer_id']} added to kitchen.")

    def notify(self, order_id):
        query = """
        SELECT o.id, o.customer_id, o.total_price, o.status, 
               GROUP_CONCAT(m.name SEPARATOR ', ') AS items
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        JOIN menuitems m ON oi.menu_item_id = m.id
        WHERE o.id = %s
        GROUP BY o.id, o.customer_id, o.total_price, o.status
        """
        order = db.fetch_one(query, (order_id,))
        if order:
            order_details = {
                'id': order[0],
                'customer_id': order[1],
                'total_price': order[2],
                'status': order[3],
                'items': order[4]
            }
            self.add_order(order_details)
            print(f"New order received:")
            print(f"Order ID: {order_details['id']}")
            print(f"Customer ID: {order_details['customer_id']}")
            print(f"Total Price: ${order_details['total_price']}")
            print(f"Status: {order_details['status']}")
            print(f"Items: {order_details['items']}")
        else:
            print(f"No order found with ID {order_id}")
