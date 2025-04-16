import tkinter as tk
from tkinter import messagebox
import pandas as pd
import numpy as np
from generate_data import generate_synthetic_data
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random

# Generate synthetic data
df = generate_synthetic_data()

# Get unique companies
companies = df["Company"].unique().tolist()

# Tkinter root window
root = tk.Tk()
root.title("Stock Market Simulator")
root.geometry("700x600")

# Default selected company
selected_company = tk.StringVar(value=companies[0])

# Portfolio Variables
portfolio_cash = 10000
portfolio_stocks = 0
latest_price = 0

# Machine Learning Model Dictionary (for each company)
models = {}
scalers = {}

# Train AI Models for Each Company
for company in companies:
    data = df[df["Company"] == company].copy()
    data.sort_values("Date", inplace=True)
    
    # Convert dates to numerical format
    data["Days"] = (data["Date"] - data["Date"].min()).dt.days

    # Feature Engineering
    data["MA20"] = data["Close"].rolling(window=20).mean()
    data["MA50"] = data["Close"].rolling(window=50).mean()
    data["MA100"] = data["Close"].rolling(window=100).mean()
    data["Daily_Change"] = data["Close"] - data["Open"]
    data["High_Low_Spread"] = data["High"] - data["Low"]
    
    data = data.bfill()

    # Select Features & Target
    X = data[["Days", "MA20", "MA50", "MA100", "Daily_Change", "High_Low_Spread", "Volume"]]
    y = data["Close"]

    # Normalize data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train Model
    model = LinearRegression()
    model.fit(X_scaled, y)

    # Store Model & Scaler
    models[company] = model
    scalers[company] = scaler

# Labels & UI Elements
label_company = tk.Label(root, text="Select Company:", font=("Arial", 12))
label_company.pack()

company_dropdown = tk.OptionMenu(root, selected_company, *companies)
company_dropdown.pack()

label_cash = tk.Label(root, text=f"Cash: ${portfolio_cash}", font=("Arial", 12))
label_cash.pack()

label_stocks = tk.Label(root, text=f"Stocks Owned: {portfolio_stocks}", font=("Arial", 12))
label_stocks.pack()

label_price = tk.Label(root, text=f"Latest Price: $0.00", font=("Arial", 14, "bold"), fg="blue")
label_price.pack()

# Entry Fields for Custom Buy/Sell
entry_amount = tk.Entry(root, font=("Arial", 12))
entry_amount.pack()
entry_amount.insert(0, "Enter Amount")

# Stock Price Updater Function (Updates Every 2 Seconds)
def update_stock_price():
    global latest_price

    company = selected_company.get()
    data = df[df["Company"] == company].copy()
    data.sort_values("Date", inplace=True)
    
    # Add Days column
    data["Days"] = (data["Date"] - data["Date"].min()).dt.days

    # Get last known values for features
    last_values = data.iloc[-1].copy()
    next_day = last_values["Days"] + 1

    # Calculate moving averages
    data["MA20"] = data["Close"].rolling(window=20).mean()
    data["MA50"] = data["Close"].rolling(window=50).mean()
    data["MA100"] = data["Close"].rolling(window=100).mean()
    data["Daily_Change"] = data["Close"] - data["Open"]
    data["High_Low_Spread"] = data["High"] - data["Low"]
    
    data = data.bfill()

    # Prepare the input data
    feature_data = pd.DataFrame([
        [
            next_day,
            data["MA20"].iloc[-1],
            data["MA50"].iloc[-1],
            data["MA100"].iloc[-1],
            data["Daily_Change"].iloc[-1],
            data["High_Low_Spread"].iloc[-1],
            data["Volume"].iloc[-1]
        ]
    ])

    # Scale the data
    feature_scaled = scalers[company].transform(feature_data)

    # Predict next price with small random variation
    latest_price = models[company].predict(feature_scaled)[0] + random.uniform(-2, 2)
    label_price.config(text=f"Latest Price: ${latest_price:.2f}")

    # Schedule the next update
    root.after(2000, update_stock_price)

# Buy Stocks Function
def buy_stock():
    global portfolio_cash, portfolio_stocks, latest_price
    try:
        buy_amount = float(entry_amount.get())
        if portfolio_cash >= buy_amount:
            stocks_bought = buy_amount // latest_price
            portfolio_cash -= stocks_bought * latest_price
            portfolio_stocks += stocks_bought
            messagebox.showinfo("Trade", f"✅ Bought {stocks_bought} stocks at ${latest_price:.2f}")
            update_ui()
        else:
            messagebox.showerror("Error", "❌ Not enough cash!")
    except ValueError:
        messagebox.showerror("Error", "❌ Enter a valid amount!")

# Sell Stocks Function
def sell_stock():
    global portfolio_cash, portfolio_stocks, latest_price
    try:
        sell_amount = float(entry_amount.get())
        stocks_to_sell = sell_amount // latest_price
        if stocks_to_sell <= portfolio_stocks:
            portfolio_cash += stocks_to_sell * latest_price
            portfolio_stocks -= stocks_to_sell
            messagebox.showinfo("Trade", f"❌ Sold {stocks_to_sell} stocks at ${latest_price:.2f}")
            update_ui()
        else:
            messagebox.showerror("Error", "❌ Not enough stocks to sell!")
    except ValueError:
        messagebox.showerror("Error", "❌ Enter a valid amount!")

# Update UI
def update_ui():
    label_cash.config(text=f"Cash: ${portfolio_cash:.2f}")
    label_stocks.config(text=f"Stocks Owned: {portfolio_stocks}")

# Show Future Price Predictions
def show_future_prices():
    company = selected_company.get()
    data = df[df["Company"] == company].copy()
    data.sort_values("Date", inplace=True)
    
    # Add Days column
    data["Days"] = (data["Date"] - data["Date"].min()).dt.days
    
    # Add technical indicators
    data["MA20"] = data["Close"].rolling(window=20).mean()
    data["MA50"] = data["Close"].rolling(window=50).mean()
    data["MA100"] = data["Close"].rolling(window=100).mean()
    data["Daily_Change"] = data["Close"] - data["Open"]
    data["High_Low_Spread"] = data["High"] - data["Low"]
    
    data = data.bfill()

    # Predict next 30 days
    last_day = data["Days"].max()
    future_days = np.array(range(last_day + 1, last_day + 31)).reshape(-1, 1)
    
    future_df = pd.DataFrame({
        "Days": future_days.flatten(),
        "MA20": [data["MA20"].iloc[-1]] * 30,
        "MA50": [data["MA50"].iloc[-1]] * 30,
        "MA100": [data["MA100"].iloc[-1]] * 30,
        "Daily_Change": [data["Daily_Change"].iloc[-1]] * 30,
        "High_Low_Spread": [data["High_Low_Spread"].iloc[-1]] * 30,
        "Volume": [data["Volume"].iloc[-1]] * 30
    })

    # Scale and predict
    future_scaled = scalers[company].transform(future_df)
    future_prices = models[company].predict(future_scaled)

    future_dates = pd.date_range(start=data["Date"].max() + timedelta(days=1), periods=30)
    
    # Plot the future predictions
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(data["Date"], data["Close"], label="Historical Prices", color="blue")
    ax.plot(future_dates, future_prices, label="Predicted Future Prices", color="green", linestyle="dashed")
    ax.set_xlabel("Date")
    ax.set_ylabel("Stock Price")
    ax.set_title(f"Future Stock Price Prediction for {company}")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Buttons
buy_button = tk.Button(root, text="BUY", command=buy_stock, font=("Arial", 12), bg="green", fg="white")
buy_button.pack(pady=10)

sell_button = tk.Button(root, text="SELL", command=sell_stock, font=("Arial", 12), bg="red", fg="white")
sell_button.pack(pady=10)

future_button = tk.Button(root, text="Show Future Prices", command=show_future_prices, font=("Arial", 12), bg="blue", fg="white")
future_button.pack(pady=10)

# Start Stock Price Updates
update_stock_price()

# Run Tkinter
root.mainloop()
