import pandas as pd
import numpy as np
import ta

def transform_data(cleaned_data, resample_freq='D'):
    
    transformed_data = {}
    for stock, df in cleaned_data.items():
        # Ensure datetime index
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        
        # Calculate technical indicators
        df['SMA_50'] = ta.trend.sma_indicator(df['Close'], window=50)
        df['SMA_200'] = ta.trend.sma_indicator(df['Close'], window=200)
        df['BB_upper'], df['BB_middle'], df['BB_lower'] = ta.volatility.bollinger_hband_indicator(df['Close']), ta.volatility.bollinger_mavg(df['Close']), ta.volatility.bollinger_lband_indicator(df['Close'])
        df['RSI'] = ta.momentum.rsi(df['Close'])
        
        # Apply feature engineering techniques
        df['Volatility'] = df['Close'].rolling(window=50).std()
        df['Price_Change'] = df['Close'].pct_change()
        
        # Resample the data
        df_resampled = df.resample(resample_freq).agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum',
            'SMA_50': 'last',
            'SMA_200': 'last',
            'BB_upper': 'last',
            'BB_middle': 'last',
            'BB_lower': 'last',
            'RSI': 'last',
            'Volatility': 'last',
            'Price_Change': 'last'
        })
        
        transformed_data[stock] = df_resampled
    
    return transformed_data

