from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("SSP")
    
    if data.num_rows > 0:
        upload_data(data, "payments_structural_indicators")
        print(f"Uploaded {data.num_rows} rows to payments_structural_indicators")
        
    save_state("payments_structural_indicators", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
