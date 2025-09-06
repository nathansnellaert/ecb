from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("FXI")
    
    if data.num_rows > 0:
        upload_data(data, "foreign_exchange_stats")
        print(f"Uploaded {data.num_rows} rows to foreign_exchange_stats")
        
    save_state("foreign_exchange_stats", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
