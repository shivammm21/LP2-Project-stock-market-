import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_synthetic_data():
    # Companies
    companies = ["AAPL", "GOOGL", "MSFT", "AMZN", "META"]
    
    # Generate dates for past 365 days
    end_date = datetime.now()
    dates = [end_date - timedelta(days=x) for x in range(365)]
    dates.reverse()
    
    data = []
    
    for company in companies:
        # Initial price between 100 and 500
        price = np.random.uniform(100, 500)
        
        for date in dates:
            # Random daily variation
            daily_volatility = np.random.uniform(0.01, 0.03)
            open_price = price * (1 + np.random.uniform(-daily_volatility, daily_volatility))
            close_price = open_price * (1 + np.random.uniform(-daily_volatility, daily_volatility))
            high_price = max(open_price, close_price) * (1 + abs(np.random.normal(0, 0.005)))
            low_price = min(open_price, close_price) * (1 - abs(np.random.normal(0, 0.005)))
            volume = int(np.random.uniform(100000, 1000000))
            
            data.append({
                'Date': date,
                'Company': company,
                'Open': open_price,
                'High': high_price,
                'Low': low_price,
                'Close': close_price,
                'Volume': volume
            })
            
            price = close_price
    
    df = pd.DataFrame(data)
    df.to_csv("synthetic_stock_data.csv", index=False)
    return df

if __name__ == "__main__":
    generate_synthetic_data()
