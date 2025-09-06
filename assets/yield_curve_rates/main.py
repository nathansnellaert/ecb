from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("YC")
    
    if data.num_rows > 0:
        upload_data(data, "yield_curve_rates")
        print(f"Uploaded {data.num_rows} rows to yield_curve_rates")
        
    save_state("yield_curve_rates", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
