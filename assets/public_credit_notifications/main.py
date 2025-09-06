from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("PCN")
    
    if data.num_rows > 0:
        upload_data(data, "public_credit_notifications")
        print(f"Uploaded {data.num_rows} rows to public_credit_notifications")
        
    save_state("public_credit_notifications", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
