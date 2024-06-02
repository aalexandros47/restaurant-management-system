class Payment:
    def __init__(self, id=None, order_id=None, payment_method=None, status='Unpaid', payment_time=None):
        self.id = id
        self.order_id = order_id
        self.payment_method = payment_method
        self.payment_time = payment_time
        self.status = status

    def process_payment(self):
        raise NotImplementedError("This method should be overridden by subclasses")

