from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("PEM")
    
    if data.num_rows > 0:
        upload_data(data, "payment_electronic_money")
        print(f"Uploaded {data.num_rows} rows to payment_electronic_money")
        
    save_state("payment_electronic_money", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
