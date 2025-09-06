from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("RESR")
    
    if data.num_rows > 0:
        upload_data(data, "real_estate_statistics")
        print(f"Uploaded {data.num_rows} rows to real_estate_statistics")
        
    save_state("real_estate_statistics", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
