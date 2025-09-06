from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("PMC")
    
    if data.num_rows > 0:
        upload_data(data, "payment_mobile_channels")
        print(f"Uploaded {data.num_rows} rows to payment_mobile_channels")
        
    save_state("payment_mobile_channels", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
