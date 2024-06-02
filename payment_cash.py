from db import *
from payment import Payment


class CashPayment(Payment):
    def process_payment(self):
        amount = db.fetch_one("SELECT total_price FROM orders WHERE id = %s", (self.order_id,))[0]
        db.execute_query("INSERT INTO payments (order_id, payment_method, amount, payment_time) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)",
                         (self.order_id, "Cash", amount))
        db.execute_query("UPDATE orders SET status = 'Paid' WHERE id = %s", (self.order_id,))
        payment_time = db.fetch_one("SELECT payment_time FROM payments WHERE order_id = %s AND payment_method = %s", (self.order_id, "Cash"))
        print(f"Payment for order {self.order_id} using Cash completed at {payment_time[0]}.")