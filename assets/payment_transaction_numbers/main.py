from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("PTN")
    
    if data.num_rows > 0:
        upload_data(data, "payment_transaction_numbers")
        print(f"Uploaded {data.num_rows} rows to payment_transaction_numbers")
        
    save_state("payment_transaction_numbers", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
