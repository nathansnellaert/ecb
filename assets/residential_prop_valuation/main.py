from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("RPV")
    
    if data.num_rows > 0:
        upload_data(data, "residential_prop_valuation")
        print(f"Uploaded {data.num_rows} rows to residential_prop_valuation")
        
    save_state("residential_prop_valuation", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
