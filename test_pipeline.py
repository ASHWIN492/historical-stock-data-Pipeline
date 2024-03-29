import unittest
from src.ingest_data import ingest_ohlc_data
from src.clean_data import clean_ohlc_data
from src.transform_data import transform_data

class TestPipeline(unittest.TestCase):
    def setUp(self):
        # Initialize attributes
        self.stocks = ['AAPL']
        self.start_date = '2022-01-01'
        self.end_date = '2022-01-10'
        self.resample_freq = 'D'

    def test_ingest_ohlc_data(self):
        # Test data ingestion
        ohlc_data = ingest_ohlc_data(self.stocks, self.start_date, self.end_date)
        self.assertTrue(isinstance(ohlc_data, dict))
        self.assertEqual(len(ohlc_data), len(self.stocks))
        # Additional checks for errors and data quality
        for stock, df in ohlc_data.items():
            self.assertFalse(df.empty, f"No data ingested for {stock}")
            self.assertFalse(df.isnull().values.any(), f"Found NaN values in {stock} data")

    def test_clean_ohlc_data(self):
        # Test data cleaning
        ohlc_data = ingest_ohlc_data(self.stocks, self.start_date, self.end_date)
        cleaned_data = clean_ohlc_data(ohlc_data)
        self.assertTrue(isinstance(cleaned_data, dict))
        for stock, df in cleaned_data.items():
            self.assertTrue(df.isnull().sum().sum() == 0)
        # Additional checks for errors and data quality
        for stock, df in cleaned_data.items():
            self.assertFalse(df.empty, f"No data after cleaning for {stock}")

    def test_transform_data(self):
        # Test data transformation
        ohlc_data = ingest_ohlc_data(self.stocks, self.start_date, self.end_date)
        cleaned_data = clean_ohlc_data(ohlc_data)
        transformed_data = transform_data(cleaned_data, self.resample_freq)
        self.assertTrue(isinstance(transformed_data, dict))
        for stock, df in transformed_data.items():
            self.assertTrue('SMA_50' in df.columns)
            self.assertTrue('SMA_200' in df.columns)
            self.assertTrue('BB_upper' in df.columns)
            self.assertTrue('BB_middle' in df.columns)
            self.assertTrue('BB_lower' in df.columns)
            self.assertTrue('RSI' in df.columns)
            self.assertTrue('Volatility' in df.columns)
            self.assertTrue('Price_Change' in df.columns)
        # Additional checks for errors and data quality
        for stock, df in transformed_data.items():
            self.assertFalse(df.empty, f"No data after transformation for {stock}")        

if __name__ == '__main__':
    unittest.main()
