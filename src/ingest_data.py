import yfinance as yf
import pandas as pd

def ingest_ohlc_data(stocks, start_date, end_date):
    
    data = {}
    for stock in stocks:
        try:
            # Fetch OHLC data
            df = yf.download(stock, start=start_date, end=end_date)
            
            # Validate data integrity
            missing_values = df.isnull().sum().sum()
            if missing_values > 0:
                print(f"Warning: Found {missing_values} missing values in {stock} data.")
            
            # Standardize data format
            df.reset_index(inplace=True)
            data[stock] = df
            
            print(f"Fetched and standardized data for {stock}")
        except Exception as e:
            print(f"Failed to fetch data for {stock}: {e}")
    return data

