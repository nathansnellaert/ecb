from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("TRD")
    
    if data.num_rows > 0:
        upload_data(data, "international_trade_flows")
        print(f"Uploaded {data.num_rows} rows to international_trade_flows")
        
    save_state("international_trade_flows", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
