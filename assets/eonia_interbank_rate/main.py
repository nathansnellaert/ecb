from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("EON")
    
    if data.num_rows > 0:
        upload_data(data, "eonia_interbank_rate")
        print(f"Uploaded {data.num_rows} rows to eonia_interbank_rate")
        
    save_state("eonia_interbank_rate", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
