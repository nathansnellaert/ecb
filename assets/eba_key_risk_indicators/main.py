from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("KRI")
    
    if data.num_rows > 0:
        upload_data(data, "eba_key_risk_indicators")
        print(f"Uploaded {data.num_rows} rows to eba_key_risk_indicators")
        
    save_state("eba_key_risk_indicators", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
