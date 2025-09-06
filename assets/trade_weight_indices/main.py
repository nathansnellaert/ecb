from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("WTS")
    
    if data.num_rows > 0:
        upload_data(data, "trade_weight_indices")
        print(f"Uploaded {data.num_rows} rows to trade_weight_indices")
        
    save_state("trade_weight_indices", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
