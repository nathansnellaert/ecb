from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("RESV")
    
    if data.num_rows > 0:
        upload_data(data, "residential_property_valuation")
        print(f"Uploaded {data.num_rows} rows to residential_property_valuation")
        
    save_state("residential_property_valuation", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
