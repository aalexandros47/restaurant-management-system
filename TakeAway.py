
from order import *
class TakeAwayOrder(Order):
    @staticmethod
    def place_takeaway_order(customer_id, item_ids):
        order_id = Order.place_order(customer_id, item_ids)
        db.execute_query("UPDATE orders SET status = %s WHERE id = %s", 
                         ('Paid', order_id))
        return order_id