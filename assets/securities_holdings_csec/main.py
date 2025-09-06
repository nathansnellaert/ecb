from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("CSEC")
    
    if data.num_rows > 0:
        upload_data(data, "securities_holdings_csec")
        print(f"Uploaded {data.num_rows} rows to securities_holdings_csec")
        
    save_state("securities_holdings_csec", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
