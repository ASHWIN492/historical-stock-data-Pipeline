from src.ingest_data import ingest_ohlc_data
from src.clean_data import clean_ohlc_data
from src.transform_data import transform_data
from src.data_visualization import  visualize_data
from src.compress_data import  compress_and_store_data
from src.data_store import  connect_to_mongodb,insert_data_into_mongodb,create_indexes

def run_pipeline(stocks, start_date, end_date, resample_freq='D', compression_directory=None, mongodb_uri=None, db_name='financial_data'):
    
    # Step 1: Ingest OHLC data
    ohlc_data = ingest_ohlc_data(stocks, start_date, end_date)
    
    # Step 2: Clean OHLC data
    cleaned_ohlc_data = clean_ohlc_data(ohlc_data)
    
    # Step 3: Transform cleaned OHLC data
    transformed_ohlc_data = transform_data(cleaned_ohlc_data, resample_freq)
    
    # Step 4: Compress and store data if compression directory is provided
    if compression_directory:
        compress_and_store_data(transformed_ohlc_data, compression_directory)
    
    # Step 5: Store data in MongoDB
    if mongodb_uri:
        # Connect to MongoDB
        collection = connect_to_mongodb(db_name, 'ohlc_data')
        # Insert transformed OHLC data into MongoDB collection
        insert_data_into_mongodb(collection, transformed_ohlc_data)
        # Create indexes for efficient querying
        create_indexes(collection)
    
    # Step 6: Visualize data
    visualize_data(transformed_ohlc_data)
    
    return transformed_ohlc_data

