from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("RESC")
    
    if data.num_rows > 0:
        upload_data(data, "commercial_property_prices")
        print(f"Uploaded {data.num_rows} rows to commercial_property_prices")
        
    save_state("commercial_property_prices", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
