from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("SHSS")
    
    if data.num_rows > 0:
        upload_data(data, "securities_holdings_sector_sheets")
        print(f"Uploaded {data.num_rows} rows to securities_holdings_sector_sheets")
        
    save_state("securities_holdings_sector_sheets", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
