from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("RA")
    
    if data.num_rows > 0:
        upload_data(data, "international_reserves_eurosystem")
        print(f"Uploaded {data.num_rows} rows to international_reserves_eurosystem")
        
    save_state("international_reserves_eurosystem", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
