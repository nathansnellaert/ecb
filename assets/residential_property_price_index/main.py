from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("RPP")
    
    if data.num_rows > 0:
        upload_data(data, "residential_property_price_index")
        print(f"Uploaded {data.num_rows} rows to residential_property_price_index")
        
    save_state("residential_property_price_index", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
