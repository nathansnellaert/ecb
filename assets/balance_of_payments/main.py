from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("BOP")
    
    if data.num_rows > 0:
        upload_data(data, "balance_of_payments")
        print(f"Uploaded {data.num_rows} rows to balance_of_payments")
        
    save_state("balance_of_payments", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
