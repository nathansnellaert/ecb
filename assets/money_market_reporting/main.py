from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("MMSR")
    
    if data.num_rows > 0:
        upload_data(data, "money_market_reporting")
        print(f"Uploaded {data.num_rows} rows to money_market_reporting")
        
    save_state("money_market_reporting", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
