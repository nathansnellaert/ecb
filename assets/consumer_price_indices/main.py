from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("ICP")
    
    if data.num_rows > 0:
        upload_data(data, "consumer_price_indices")
        print(f"Uploaded {data.num_rows} rows to consumer_price_indices")
        
    save_state("consumer_price_indices", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
