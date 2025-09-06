from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("FM")
    
    if data.num_rows > 0:
        upload_data(data, "financial_market_data")
        print(f"Uploaded {data.num_rows} rows to financial_market_data")
        
    save_state("financial_market_data", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
