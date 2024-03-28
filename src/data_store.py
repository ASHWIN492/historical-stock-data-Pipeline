import pymongo
import pandas as pd

# Function to connect to MongoDB
def connect_to_mongodb(database_name, collection_name):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client[database_name]
    collection = db[collection_name]
    return collection

# Function to insert data into MongoDB collection
def insert_data_into_mongodb(collection, data):
    for stock, df in data.items():
        
        df_copy = df.copy()
        df_copy.index = pd.to_datetime(df_copy.index)
        
        # Partition data by year and month
        for year, year_group in df_copy.groupby(df_copy.index.year):
            for month, month_group in year_group.groupby(year_group.index.month):
               
                document = {
                    'stock': stock,
                    'year': year,
                    'month': month,
                    'data': month_group.to_dict(orient='records')
                }
                
                collection.insert_one(document)
                
# Create indexes for efficient querying
def create_indexes(collection):
    
    collection.create_index([('stock', pymongo.ASCENDING), ('year', pymongo.ASCENDING), ('month', pymongo.ASCENDING)])
   


