import random
import time

class StockMarketSimulation:
    def __init__(self, starting_balance=10000):
        self.balance = starting_balance
        self.portfolio = {}
        self.stock_prices = {"AAPL": 150, "GOOG": 2800, "TSLA": 700, "AMZN": 3300}
        self.history = []

    def display_status(self):
        print("\n--- Current Status ---")
        print(f"Balance: ${self.balance}")
        print(f"Portfolio: {self.portfolio}")
        print("Stock Prices:")
        for stock, price in self.stock_prices.items():
            print(f"{stock}: ${price}")
        print("----------------------")

    def buy_stock(self, stock, quantity):
        if stock not in self.stock_prices:
            print(f"Error: {stock} is not a valid stock.")
            return
        stock_price = self.stock_prices[stock]
        cost = stock_price * quantity
        if self.balance >= cost:
            self.balance -= cost
            if stock in self.portfolio:
                self.portfolio[stock] += quantity
            else:
                self.portfolio[stock] = quantity
            print(f"Bought {quantity} shares of {stock} at ${stock_price} each.")
        else:
            print("Error: Not enough balance to complete the purchase.")

    def sell_stock(self, stock, quantity):
        if stock not in self.portfolio or self.portfolio[stock] < quantity:
            print(f"Error: You don't own enough shares of {stock}.")
            return
        stock_price = self.stock_prices[stock]
        revenue = stock_price * quantity
        self.balance += revenue
        self.portfolio[stock] -= quantity
        if self.portfolio[stock] == 0:
            del self.portfolio[stock]
        print(f"Sold {quantity} shares of {stock} at ${stock_price} each.")

    def update_stock_prices(self):
        print("\nUpdating stock prices...")
        for stock in self.stock_prices:
            change_percent = random.uniform(-0.05, 0.05)  # Price can change +/- 5%
            self.stock_prices[stock] = round(self.stock_prices[stock] * (1 + change_percent), 2)
        print("Stock prices updated.")

    def show_history(self):
        if not self.history:
            print("No history available.")
        else:
            for entry in self.history:
                print(entry)

    def run(self):
        print("Welcome to the Stock Market Simulation!")
        while True:
            self.display_status()
            print("\nActions: ")
            print("1. Buy Stock")
            print("2. Sell Stock")
            print("3. Update Stock Prices")
            print("4. Show History")
            print("5. Exit")

            action = input("Select an action: ")

            if action == '1':
                stock = input("Enter stock symbol (AAPL, GOOG, TSLA, AMZN): ").upper()
                quantity = int(input("Enter quantity: "))
                self.buy_stock(stock, quantity)
                self.history.append(f"Bought {quantity} shares of {stock}.")
            elif action == '2':
                stock = input("Enter stock symbol (AAPL, GOOG, TSLA, AMZN): ").upper()
                quantity = int(input("Enter quantity: "))
                self.sell_stock(stock, quantity)
                self.history.append(f"Sold {quantity} shares of {stock}.")
            elif action == '3':
                self.update_stock_prices()
            elif action == '4':
                self.show_history()
            elif action == '5':
                print("Exiting the simulation. Goodbye!")
                break
            else:
                print("Invalid action. Please try again.")
            
            time.sleep(2)  # Add delay to simulate real-time updates

if __name__ == "__main__":
    simulation = StockMarketSimulation()
    simulation.run()

