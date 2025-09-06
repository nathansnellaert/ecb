from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("DWA")
    
    if data.num_rows > 0:
        upload_data(data, "data_warehouse_aggregates")
        print(f"Uploaded {data.num_rows} rows to data_warehouse_aggregates")
        
    save_state("data_warehouse_aggregates", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
