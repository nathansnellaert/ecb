from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("SHS")
    
    if data.num_rows > 0:
        upload_data(data, "securities_holdings")
        print(f"Uploaded {data.num_rows} rows to securities_holdings")
        
    save_state("securities_holdings", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
