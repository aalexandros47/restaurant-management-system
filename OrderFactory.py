from DineInOrder import DineInOrder
from TakeAway import TakeAwayOrder

class OrderFactory:
    @staticmethod
    def create_order(order_type, customer_id, item_ids, table_id=None):
        if order_type == "DineIn":
            return DineInOrder.place_dine_in_order(customer_id, item_ids, table_id)
        elif order_type == "TakeAway":
            return TakeAwayOrder.place_takeaway_order(customer_id, item_ids)
        else:
            raise ValueError("Invalid order type")
