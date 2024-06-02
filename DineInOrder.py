from order import *

class DineInOrder(Order):
    @staticmethod
    def place_dine_in_order(customer_id, item_ids, table_id):
        order_id = Order.place_order(customer_id, item_ids)
        db.execute_query("UPDATE orders SET table_id = %s WHERE id = %s", 
                         (table_id, order_id))
        return order_id