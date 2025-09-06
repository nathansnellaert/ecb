from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("PTT")
    
    if data.num_rows > 0:
        upload_data(data, "payment_transaction_totals")
        print(f"Uploaded {data.num_rows} rows to payment_transaction_totals")
        
    save_state("payment_transaction_totals", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
