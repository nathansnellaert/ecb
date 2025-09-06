from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("EXR")
    
    if data.num_rows > 0:
        upload_data(data, "exchange_rates")
        print(f"Uploaded {data.num_rows} rows to exchange_rates")
        
    save_state("exchange_rates", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
