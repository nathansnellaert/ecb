from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("SUP")
    
    if data.num_rows > 0:
        upload_data(data, "banking_supervisory_metrics")
        print(f"Uploaded {data.num_rows} rows to banking_supervisory_metrics")
        
    save_state("banking_supervisory_metrics", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
