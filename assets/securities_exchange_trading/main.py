from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("SEE")
    
    if data.num_rows > 0:
        upload_data(data, "securities_exchange_trading")
        print(f"Uploaded {data.num_rows} rows to securities_exchange_trading")
        
    save_state("securities_exchange_trading", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
