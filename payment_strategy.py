from payment_cash import *
from payment_creditcard import *
from payment_digitalwallet import *

class PaymentStrategy:
    @staticmethod
    def get_payment_method(payment_type, order_id):
        if payment_type == "Card":
            return CreditCardPayment(order_id=order_id)
        elif payment_type == "Cash":
            return CashPayment(order_id=order_id)
        elif payment_type == "DWallet":
            return DigitalWalletPayment(order_id=order_id)
        else:
            raise ValueError("Invalid payment method")
