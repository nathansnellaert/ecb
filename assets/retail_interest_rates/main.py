from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("RIR")
    
    if data.num_rows > 0:
        upload_data(data, "retail_interest_rates")
        print(f"Uploaded {data.num_rows} rows to retail_interest_rates")
        
    save_state("retail_interest_rates", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
