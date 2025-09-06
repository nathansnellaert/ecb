from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("CCP")
    
    if data.num_rows > 0:
        upload_data(data, "central_counterparty_clearing")
        print(f"Uploaded {data.num_rows} rows to central_counterparty_clearing")
        
    save_state("central_counterparty_clearing", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
