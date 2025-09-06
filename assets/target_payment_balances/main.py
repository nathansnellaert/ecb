from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("TGB")
    
    if data.num_rows > 0:
        upload_data(data, "target_payment_balances")
        print(f"Uploaded {data.num_rows} rows to target_payment_balances")
        
    save_state("target_payment_balances", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
