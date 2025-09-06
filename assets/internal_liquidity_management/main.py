from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("ILM")
    
    if data.num_rows > 0:
        upload_data(data, "internal_liquidity_management")
        print(f"Uploaded {data.num_rows} rows to internal_liquidity_management")
        
    save_state("internal_liquidity_management", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
