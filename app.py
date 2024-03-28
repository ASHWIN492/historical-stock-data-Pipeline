import datetime
import streamlit as st
from pipeline import run_pipeline
from test_pipeline import TestPipeline
import unittest

def run_tests():
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestPipeline)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    return result

def main():
    st.title("Financial Data Pipeline")

    # Sidebar inputs
    st.sidebar.title("Pipeline Configuration")
    stocks_input = st.sidebar.text_input("Enter stock tickers (comma-separated)", "AAPL,AMZN,NFLX,GOOG,MSFT")
    stocks = [s.strip() for s in stocks_input.split(",")]
    start_date = st.sidebar.date_input("Start Date", value=datetime.date(1990, 1, 1))
    end_date = st.sidebar.date_input("End Date", value=datetime.date.today())
    resample_freq = st.sidebar.selectbox("Resample Frequency", ["D", "W", "M"], index=0)
    compression_directory = st.sidebar.text_input("Compression Directory", "compressed_data")
    mongodb_uri = st.sidebar.text_input("MongoDB URI", "mongodb://localhost:27017/")
    db_name = st.sidebar.text_input("Database Name", "financial_data")

    transformed_data = None

    # Run pipeline
    if st.button("Run Pipeline"):
        st.write("Running pipeline...")
        transformed_data = run_pipeline(stocks, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), resample_freq, compression_directory, mongodb_uri, db_name)
        st.write("Pipeline completed successfully.")
    
        

    # Display visualization
    if transformed_data:
        st.subheader("Visualization")
        for stock, df in transformed_data.items():
            st.write(f"OHLC Data Visualization for {stock}")
            st.line_chart(df[['Close', 'Open', 'SMA_50', 'SMA_200', 'BB_upper', 'BB_lower']])
            
    # Run tests
    if st.button("Run Tests"):
        st.write("Running tests...")
        test_results = run_tests()
        st.write(f"Tests completed. Results: {test_results}")        

if __name__ == "__main__":
    main()
