from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("EWT")
    
    if data.num_rows > 0:
        upload_data(data, "ecb_wage_tracker")
        print(f"Uploaded {data.num_rows} rows to ecb_wage_tracker")
        
    save_state("ecb_wage_tracker", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
