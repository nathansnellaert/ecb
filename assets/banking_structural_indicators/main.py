from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("SSI")
    
    if data.num_rows > 0:
        upload_data(data, "banking_structural_indicators")
        print(f"Uploaded {data.num_rows} rows to banking_structural_indicators")
        
    save_state("banking_structural_indicators", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
