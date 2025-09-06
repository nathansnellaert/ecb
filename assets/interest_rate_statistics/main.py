from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("IRS")
    
    if data.num_rows > 0:
        upload_data(data, "interest_rate_statistics")
        print(f"Uploaded {data.num_rows} rows to interest_rate_statistics")
        
    save_state("interest_rate_statistics", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
