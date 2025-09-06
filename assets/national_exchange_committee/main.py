from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("NEC")
    
    if data.num_rows > 0:
        upload_data(data, "national_exchange_committee")
        print(f"Uploaded {data.num_rows} rows to national_exchange_committee")
        
    save_state("national_exchange_committee", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
