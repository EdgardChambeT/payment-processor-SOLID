from abc import ABC, abstractmethod
import os

# Applying Dependency Inversion Principle (DIP)
class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount: float):
        pass

# Implementing different payment methods with commissions/discounts
class CreditCardPayment(PaymentMethod):
    def pay(self, amount: float):
        commission = amount * 0.02  # 2% commission
        total = amount + commission
        print(f"💳 Paying ${total:.2f} using Credit Card (2% commission).")

class PayPalPayment(PaymentMethod):
    def pay(self, amount: float):
        commission = amount * 0.03  # 3% commission
        total = amount + commission
        print(f"🅿️ Paying ${total:.2f} using PayPal (3% commission).")

class CryptoPayment(PaymentMethod):
    def pay(self, amount: float):
        discount = amount * 0.05  # 5% discount
        total = amount - discount
        print(f"₿ Paying ${total:.2f} using Cryptocurrency (5% discount).")

# Payment processor that follows Open/Closed Principle (OCP)
class PaymentProcessor:
    def __init__(self, payment_method: PaymentMethod):
        self.payment_method = payment_method

    def process_payment(self, amount: float):
        if amount <= 0:
            print("❌ Error: The amount must be greater than zero.")
            return
        self.payment_method.pay(amount)

# Function to get a valid amount
def get_valid_amount():
    env_amount = os.getenv("PAYMENT_AMOUNT")  # Read from environment variable

    if env_amount:
        try:
            amount = float(env_amount)
            if amount > 0:
                print(f"✅ Amount received from environment: ${amount}")
                return amount
            else:
                print("❌ The amount must be a positive number.")
        except ValueError:
            print("❌ Invalid environment input. Please enter a valid number.")

    while True:
        try:
            amount = float(input("Enter the amount to pay: $"))
            if amount > 0:
                return amount
            else:
                print("❌ The amount must be a positive number.")
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")

# Dynamic method selection using environment variable
def select_payment_method():
    env_method = os.getenv("PAYMENT_METHOD")  # Read from environment variable

    if env_method:
        if env_method == "1":
            return CreditCardPayment()
        elif env_method == "2":
            return PayPalPayment()
        elif env_method == "3":
            return CryptoPayment()
        else:
            print("❌ Invalid PAYMENT_METHOD environment variable.")
            exit(1)

    print("\nSelect a payment method:")
    print("1. Credit Card")
    print("2. PayPal")
    print("3. Cryptocurrency")
    option = input("Enter your choice (1/2/3): ")

    if option == "1":
        return CreditCardPayment()
    elif option == "2":
        return PayPalPayment()
    elif option == "3":
        return CryptoPayment()
    else:
        print("❌ Invalid choice. Please try again.")
        return select_payment_method()

# Main program
print("=== Payment Processing System ===")
amount = get_valid_amount()
payment_method = select_payment_method()
processor = PaymentProcessor(payment_method)
processor.process_payment(amount)
