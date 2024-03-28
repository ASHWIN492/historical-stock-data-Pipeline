import os
import pyarrow.parquet as pq
import matplotlib.pyplot as plt
import seaborn as sns
import pyarrow as pa

def compress_and_store_data(transformed_data, directory):
    
    os.makedirs(directory, exist_ok=True)
    for stock, df in transformed_data.items():
        file_path = os.path.join(directory, f"{stock}.parquet")
        table = pa.Table.from_pandas(df)
        pq.write_table(table, file_path, compression='snappy')
        print(f"Data for {stock} compressed and stored at: {file_path}")
