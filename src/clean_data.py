import pandas as pd
import numpy as np

def clean_ohlc_data(data):
    
    cleaned_data = {}
    for stock, df in data.items():
        # Handle missing values by forward filling
        df.fillna(method='ffill', inplace=True)
        
        # Exclude non-numeric columns from z-score calculation
        numeric_cols = df.select_dtypes(include=np.number).columns
        z_scores = (df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std()
        
        # Detect and correct outliers using z-score
        outliers = z_scores.abs() > 3
        df.loc[outliers.any(axis=1), numeric_cols] = np.nan  # Replace outliers with NaN
        
        # Handle any remaining missing values after outlier correction
        df.fillna(method='ffill', inplace=True)
        
        cleaned_data[stock] = df
    return cleaned_data


