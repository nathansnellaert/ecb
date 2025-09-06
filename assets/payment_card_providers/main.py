from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("PCP")
    
    if data.num_rows > 0:
        upload_data(data, "payment_card_providers")
        print(f"Uploaded {data.num_rows} rows to payment_card_providers")
        
    save_state("payment_card_providers", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
