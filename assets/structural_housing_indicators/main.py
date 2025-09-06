from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("SHI")
    
    if data.num_rows > 0:
        upload_data(data, "structural_housing_indicators")
        print(f"Uploaded {data.num_rows} rows to structural_housing_indicators")
        
    save_state("structural_housing_indicators", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
