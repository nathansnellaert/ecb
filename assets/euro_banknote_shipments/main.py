from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("BNT")
    
    if data.num_rows > 0:
        upload_data(data, "euro_banknote_shipments")
        print(f"Uploaded {data.num_rows} rows to euro_banknote_shipments")
        
    save_state("euro_banknote_shipments", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
