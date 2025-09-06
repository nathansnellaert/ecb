from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("ESB")
    
    if data.num_rows > 0:
        upload_data(data, "eu_balance_payments")
        print(f"Uploaded {data.num_rows} rows to eu_balance_payments")
        
    save_state("eu_balance_payments", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
