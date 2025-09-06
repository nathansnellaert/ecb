from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("BSI")
    
    if data.num_rows > 0:
        upload_data(data, "balance_sheet_items")
        print(f"Uploaded {data.num_rows} rows to balance_sheet_items")
        
    save_state("balance_sheet_items", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
